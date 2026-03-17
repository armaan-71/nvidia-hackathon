import { NonprofitProfile, GrantOpportunity, ChatMessage, TimelineItem } from './types';
import { mockProfile, mockTimeline } from './mockData';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Persistent session ID for this browser tab
const SESSION_ID = `session-${Date.now()}`;

// ------------------------------------------------------------------
// Adapter: maps the FastAPI AgentResponse to the frontend ChatMessage
// ------------------------------------------------------------------
interface BackendAgentResponse {
  message: string;
  active_agent: string;
  session_id: string;
  data?: Record<string, unknown>;
  suggested_actions?: string[];
  timestamp?: string;
}

function agentResponseToChat(res: BackendAgentResponse): ChatMessage {
  return {
    id: `msg-${Date.now()}`,
    role: 'agent',
    content: res.message,
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    sources: res.data
      ? Object.entries(res.data).map(([key, val], i) => ({
          id: `src-${Date.now()}-${i}`,
          title: `${key.replace('_', ' ')} data`,
          snippet: typeof val === 'string' ? val.slice(0, 200) : JSON.stringify(val).slice(0, 200),
          type: key,
        }))
      : undefined,
    activeAgent: res.active_agent,
    suggestedActions: res.suggested_actions,
  };
}

// ------------------------------------------------------------------
// Chat
// ------------------------------------------------------------------

let chatMessagesCache: ChatMessage[] = [];

export async function getChatMessages(): Promise<ChatMessage[]> {
  return chatMessagesCache;
}

export async function sendChatMessage(
  _history: ChatMessage[],
  newText: string
): Promise<ChatMessage> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: newText, session_id: SESSION_ID }),
  });

  if (!res.ok) {
    throw new Error(`Backend error: ${res.status}`);
  }

  const data: BackendAgentResponse = await res.json();
  const chatMsg = agentResponseToChat(data);
  chatMessagesCache = [..._history, chatMsg];
  return chatMsg;
}

// ------------------------------------------------------------------
// Grants  (fetched from backend session store after a discovery chat)
// ------------------------------------------------------------------

export async function getGrantOpportunities(): Promise<GrantOpportunity[]> {
  try {
    const res = await fetch(`${API_BASE}/grants?session_id=${SESSION_ID}`);
    if (!res.ok) return [];
    const data = await res.json();

    // Map raw backend grant objects to the frontend GrantOpportunity shape
    if (Array.isArray(data) && data.length > 0) {
      return data.map((g: Record<string, unknown>, i: number) => ({
        id: `g-${i}`,
        title: (g.title as string) || 'Untitled Grant',
        funder: (g.url as string) || 'Unknown',
        deadline: 'TBD',
        fundingAmount: 'See details',
        matchScore: Math.round(((g.score as number) || 0) * 100),
        summary: (g.content as string) || '',
        eligibility: '',
        strengths: [],
        risks: [],
        sourceUrl: (g.url as string) || '#',
        status: 'open' as const,
      }));
    }
  } catch (err) {
    console.warn('Could not fetch grants from backend, using empty list:', err);
  }
  return [];
}

// ------------------------------------------------------------------
// Profile (mock for now — could wire to a future /profile endpoint)
// ------------------------------------------------------------------

export async function getNonprofitProfile(): Promise<NonprofitProfile> {
  return mockProfile;
}

// ------------------------------------------------------------------
// Timeline (mock for now)
// ------------------------------------------------------------------

export async function getSubmissionTimeline(_grantId: string): Promise<TimelineItem[]> {
  return mockTimeline;
}

// ------------------------------------------------------------------
// Document Upload → /ingest
// ------------------------------------------------------------------

export async function uploadDocuments(files: FileList | null): Promise<boolean> {
  if (!files || files.length === 0) return false;

  for (let i = 0; i < files.length; i++) {
    const formData = new FormData();
    formData.append('file', files[i]);

    const res = await fetch(`${API_BASE}/ingest`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      console.error(`Ingest failed for ${files[i].name}: ${res.status}`);
      return false;
    }
  }
  return true;
}
