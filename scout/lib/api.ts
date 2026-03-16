import { NonprofitProfile, GrantOpportunity, ChatMessage, TimelineItem } from './types';
import { mockProfile, mockGrants, mockTimeline, mockChats } from './mockData';

// Helper to simulate network latency
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export async function getNonprofitProfile(): Promise<NonprofitProfile> {
  await delay(400); // simulate latency
  return mockProfile;
}

export async function getGrantOpportunities(): Promise<GrantOpportunity[]> {
  await delay(600);
  return mockGrants;
}

export async function getGrantById(id: string): Promise<GrantOpportunity | null> {
  await delay(300);
  const grant = mockGrants.find((g) => g.id === id);
  return grant || null;
}

export async function getSubmissionTimeline(grantId: string): Promise<TimelineItem[]> {
  await delay(500);
  // In a real app we'd filter by grantId, for mock we just return the shared timeline
  return mockTimeline;
}

// Simple state to hold new chat messages (in-memory for the session)
let chatMessagesCache = [...mockChats];

export async function getChatMessages(): Promise<ChatMessage[]> {
  await delay(400);
  return chatMessagesCache;
}

export async function sendChatMessage(messages: ChatMessage[], newText: string): Promise<ChatMessage> {
  await delay(800);
  
  // Create the simulated agent response
  const agentResponse: ChatMessage = {
    id: `msg-${Date.now()}`,
    role: 'agent',
    content: `I've analyzed your request: "${newText}". Based on your nonprofit profile, I recommend looking at the previously mentioned Monterey Bay Restoration Grant. It perfectly fits your immediate needs.`,
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    sources: [
      {
        id: `s-${Date.now()}`,
        title: 'Monterey Bay Restoration Grant Overview',
        snippet: 'Local nonprofits active in Monterey Bay with immediate conservation goals.',
        type: 'grant_doc',
      }
    ]
  };
  
  // In a real app, we might persist these to a DB. Here we update cache for client demo
  chatMessagesCache = [...messages, agentResponse];
  return agentResponse;
}

export async function uploadDocuments(files: FileList | null): Promise<boolean> {
  await delay(1500);
  return true;
}
