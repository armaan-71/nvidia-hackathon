export interface NonprofitProfile {
  id: string;
  name: string;
  mission: string;
  location: string;
  focusAreas: string[];
  annualBudget: string;
  nonprofitStatus: string;
  summary: string;
}

export interface GrantOpportunity {
  id: string;
  title: string;
  funder: string;
  deadline: string;
  fundingAmount: string;
  matchScore: number;
  summary: string;
  eligibility: string;
  strengths: string[];
  risks: string[];
  sourceUrl: string;
  status: 'open' | 'closed' | 'upcoming';
}

export interface SourceReference {
  id: string;
  title: string;
  snippet: string;
  type: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
  sources?: SourceReference[];
  activeAgent?: string;
  suggestedActions?: string[];
}

export interface TimelineItem {
  id: string;
  title: string;
  dueDate: string;
  status: 'complete' | 'in progress' | 'upcoming';
  description: string;
}
