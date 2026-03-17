'use client';

import { useState, useEffect, useRef } from 'react';
import { ChatMessage, SourceReference } from '@/lib/types';
import { getChatMessages, sendChatMessage } from '@/lib/api';

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [activeSources, setActiveSources] = useState<SourceReference[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let mounted = true;
    getChatMessages().then(msgs => {
      if (mounted) {
        setMessages(msgs);
        setLoading(false);
        // Set the active sources to the last agent message's sources if available
        const lastAgentMsg = [...msgs].reverse().find(m => m.role === 'agent' && m.sources);
        if (lastAgentMsg && lastAgentMsg.sources) {
          setActiveSources(lastAgentMsg.sources);
        }
      }
    });
    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isSending]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isSending) return;

    const userMsg: ChatMessage = {
      id: `usr-${Date.now()}`,
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsSending(true);

    try {
      const response = await sendChatMessage(messages, userMsg.content);
      setMessages(prev => [...prev, response]);
      if (response.sources) {
        setActiveSources(response.sources);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsSending(false);
    }
  };

  const handleSourceClick = (msg: ChatMessage) => {
    if (msg.sources) {
      setActiveSources(msg.sources);
    }
  };

  const handleActionClick = (action: string) => {
    setInput(action);
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setIsUploading(true);
    setUploadStatus('idle');
    try {
      const { uploadDocuments } = await import('@/lib/api');
      const success = await uploadDocuments(files);
      if (success) {
        setUploadStatus('success');
        setTimeout(() => setUploadStatus('idle'), 3000);
      } else {
        setUploadStatus('error');
      }
    } catch (err) {
      console.error('Upload failed:', err);
      setUploadStatus('error');
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] overflow-hidden">
      {/* Left Pane - Chat Area */}
      <div className="flex-1 flex flex-col border-r border-neutral-800 bg-neutral-950">
        <div className="p-4 border-b border-neutral-800 bg-neutral-900/50 flex items-center justify-between">
          <div>
            <h2 className="font-semibold text-white">Agent Workspace</h2>
            <p className="text-xs text-neutral-400">Ask me to find grants, check eligibility, or draft proposals.</p>
          </div>
          <div className="flex items-center gap-2">
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleUpload} 
              className="hidden" 
              multiple 
              accept=".pdf,.doc,.docx,.txt,.md"
            />
            <button 
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading}
              className={`
                flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all
                ${uploadStatus === 'success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 
                  uploadStatus === 'error' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                  'bg-white text-black hover:bg-neutral-200'}
                disabled:opacity-50
              `}
            >
              {isUploading ? (
                <>
                  <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Uploading...
                </>
              ) : uploadStatus === 'success' ? (
                <>
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                  Done
                </>
              ) : (
                <>
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                  Ingest Docs
                </>
              )}
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {loading ? (
             <div className="flex justify-center text-neutral-500 py-10">Loading history...</div>
          ) : (
            messages.map((msg) => (
              <div 
                key={msg.id} 
                className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
                onClick={() => msg.role === 'agent' && handleSourceClick(msg)}
              >
                <div className={`
                  max-w-[85%] rounded-2xl px-5 py-3 
                  ${msg.role === 'user' ? 'bg-white text-black rounded-br-sm' : 'bg-neutral-900 border border-neutral-800 text-white rounded-bl-sm cursor-pointer hover:border-neutral-700 transition-colors'}
                `}>
                  {msg.role === 'agent' && msg.activeAgent && (
                    <div className="mb-2">
                      <span className="inline-flex items-center rounded-md bg-violet-500/10 border border-violet-500/20 px-2 py-0.5 text-[10px] font-semibold tracking-wider uppercase text-violet-400">
                        {msg.activeAgent.replace('_', ' ')}
                      </span>
                    </div>
                  )}
                  <p className="leading-relaxed whitespace-pre-wrap text-sm">{msg.content}</p>
                  
                  {msg.role === 'agent' && msg.sources && msg.sources.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-neutral-800 flex gap-2">
                       <span className="text-xs font-medium text-emerald-400">
                         {msg.sources.length} source{msg.sources.length > 1 ? 's' : ''} referenced
                       </span>
                    </div>
                  )}

                  {msg.role === 'agent' && msg.suggestedActions && msg.suggestedActions.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-neutral-800 flex flex-wrap gap-2">
                      {msg.suggestedActions.map((action, i) => (
                        <button
                          key={i}
                          onClick={(e) => { e.stopPropagation(); handleActionClick(action); }}
                          className="text-xs bg-neutral-800 border border-neutral-700 text-neutral-300 rounded-lg px-3 py-1.5 hover:bg-neutral-700 hover:text-white transition-colors"
                        >
                          {action}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                <span className="text-[10px] text-neutral-500 mt-2 mx-2">{msg.timestamp}</span>
              </div>
            ))
          )}
          
          {isSending && (
            <div className="flex items-start">
               <div className="bg-neutral-900 border border-neutral-800 rounded-2xl rounded-bl-sm px-5 py-4">
                 <div className="flex gap-1.5">
                   <div className="w-2 h-2 rounded-full bg-neutral-500 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                   <div className="w-2 h-2 rounded-full bg-neutral-500 animate-bounce" style={{ animationDelay: '150ms' }}></div>
                   <div className="w-2 h-2 rounded-full bg-neutral-500 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                 </div>
               </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="p-4 bg-neutral-950 border-t border-neutral-800">
          <form onSubmit={handleSend} className="relative flex items-center">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Message Scout..."
              className="w-full bg-neutral-900 border border-neutral-800 text-white text-sm rounded-xl pl-4 pr-12 py-4 focus:outline-none focus:border-neutral-600 focus:ring-1 focus:ring-neutral-600 transition-all placeholder:text-neutral-500"
              disabled={isSending}
            />
            <button 
              type="submit"
              disabled={!input.trim() || isSending}
              className="absolute right-2 p-2 bg-white text-black rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-neutral-200 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </button>
          </form>
        </div>
      </div>

      {/* Right Pane - Sources */}
      <div className="hidden lg:flex w-1/3 flex-col bg-neutral-900 border-l border-neutral-800">
        <div className="p-4 border-b border-neutral-800">
          <h2 className="font-semibold text-white">Sources & Context</h2>
          <p className="text-xs text-neutral-400">References for the selected message.</p>
        </div>
        
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {activeSources.length === 0 ? (
            <div className="text-center text-neutral-500 py-10 text-sm">
              No sources for this context. Click on an agent message to view its sources.
            </div>
          ) : (
            activeSources.map(src => (
              <div key={src.id} className="bg-neutral-950 border border-neutral-800 rounded-xl p-4 shadow-sm">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-semibold tracking-widest uppercase text-emerald-500">
                    {src.type.replace('_', ' ')}
                  </span>
                </div>
                <h4 className="text-sm font-bold text-white mb-2 leading-tight">{src.title}</h4>
                <div className="bg-neutral-900 border border-neutral-800 rounded p-3 text-xs text-neutral-300 font-mono leading-relaxed relative before:content-[''] before:absolute before:left-0 before:top-0 before:bottom-0 before:w-1 before:bg-neutral-700 before:rounded-l">
                  "{src.snippet}"
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
