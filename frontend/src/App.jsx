import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, RefreshCw, Server, User, Bot, Info, LayoutDashboard, MessageSquare } from 'lucide-react';

const API_BASE = "http://localhost:8000";

function App() {
    const [messages, setMessages] = useState([
        { role: 'bot', content: "Hello! I'm your Official LBRCE Assistant. I can help you with campus notices and latest faculty updates or class changes. How can I assist you today?" }
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [syncing, setSyncing] = useState(false);
    const [status, setStatus] = useState("Checking...");
    const chatEndRef = useRef(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        checkStatus();
    }, []);

    const checkStatus = async () => {
        try {
            const res = await axios.get(`${API_BASE}/status`);
            setStatus(res.data.status === "online" ? "System Ready" : "System Error");
        } catch (err) {
            setStatus("Offline");
        }
    };

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const response = await axios.post(`${API_BASE}/chat`, { question: input });
            setMessages(prev => [...prev, { role: 'bot', content: response.data.answer }]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'bot', content: "Error: Unable to reach the server. Please ensure the backend is running." }]);
        } finally {
            setLoading(false);
        }
    };

    const handleSync = async () => {
        setSyncing(true);
        try {
            const response = await axios.get(`${API_BASE}/sync`);
            alert(response.data.message);
        } catch (error) {
            alert("Failed to sync documents. Check the backend logs.");
        } finally {
            setSyncing(false);
        }
    };

    return (
        <div className="flex h-screen bg-slate-900 text-slate-100 overflow-hidden font-sans">
            {/* Sidebar */}
            <aside className="w-72 bg-slate-800 border-r border-slate-700 flex flex-col p-6 shadow-2xl">
                <div className="flex items-center gap-3 mb-10 pb-6 border-b border-slate-700">
                    <div className="p-2 bg-blue-600 rounded-lg shadow-lg shadow-blue-500/20">
                        <LayoutDashboard size={24} className="text-white" />
                    </div>
                    <h1 className="text-xl font-bold tracking-tight">LBRCE Agent</h1>
                </div>

                <nav className="flex-1 space-y-4">
                    <div className="p-4 bg-slate-700/50 rounded-xl border border-slate-600/50">
                        <div className="flex items-center gap-2 mb-3 text-xs font-semibold text-slate-400 uppercase tracking-widest">
                            <Server size={14} />
                            System Status
                        </div>
                        <div className="flex items-center gap-2">
                            <div className={`h-2.5 w-2.5 rounded-full ${status === 'System Ready' ? 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]' : 'bg-rose-500 animate-pulse'}`}></div>
                            <span className="text-sm font-medium">{status}</span>
                        </div>
                    </div>

                    <button
                        onClick={handleSync}
                        disabled={syncing}
                        className="w-full flex items-center justify-between p-4 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-xl transition-all duration-300 shadow-lg shadow-blue-900/20 group"
                    >
                        <div className="flex items-center gap-2">
                            <RefreshCw size={18} className={syncing ? "animate-spin" : "group-hover:rotate-180 transition-transform duration-500"} />
                            <span className="font-semibold">Sync Now</span>
                        </div>
                        {syncing && <span className="text-xs font-light opacity-80 italic">Syncing...</span>}
                    </button>
                </nav>

                <div className="mt-auto p-4 bg-slate-700/30 rounded-xl border border-dashed border-slate-600">
                    <p className="text-[10px] text-slate-400 leading-relaxed">
                        Features: Supports <span className="text-blue-400 font-bold">PDF Notices</span> & <span className="text-emerald-400 font-bold">Live Messages</span>.
                    </p>
                    <p className="text-[10px] text-slate-500 mt-1">
                        Assumption: If year is missing, current year is 2026.
                    </p>
                </div>
            </aside>

            {/* Main Chat Area */}
            <main className="flex-1 flex flex-col relative bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-slate-900 via-slate-900 to-slate-800">
                {/* Header */}
                <header className="h-20 bg-slate-900/50 backdrop-blur-md border-b border-slate-700/50 flex items-center justify-between px-10 z-10 sticky top-0">
                    <div className="flex items-center gap-2">
                        <MessageSquare size={20} className="text-blue-400" />
                        <h2 className="text-lg font-semibold">Campus Bot Chat</h2>
                    </div>
                    <div className="text-xs text-slate-500 font-mono flex items-center gap-2">
                        LLM: <span className="text-blue-500 px-2 py-1 bg-blue-500/10 rounded border border-blue-500/20">Groq (Llama 3.3 70B)</span>
                    </div>
                </header>

                {/* Scrollable Messages */}
                <div className="flex-1 overflow-y-auto px-6 py-10 space-y-8 scroll-smooth">
                    {messages.map((msg, i) => (
                        <div
                            key={i}
                            className={`flex items-start gap-4 max-w-4xl mx-auto animate-in fade-in slide-in-from-bottom-2 duration-300 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                        >
                            <div className={`p-3 rounded-2xl shadow-xl shrink-0 ${msg.role === 'user' ? 'bg-blue-600 shadow-blue-900/20' : 'bg-slate-700 shadow-black/20'}`}>
                                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} className="text-blue-400" />}
                            </div>
                            <div className="flex flex-col gap-2 group">
                                <span className={`text-[11px] font-bold tracking-widest uppercase text-slate-500 ${msg.role === 'user' ? 'text-right' : ''}`}>
                                    {msg.role === 'user' ? 'Student' : 'Campus Bot'}
                                </span>
                                <div className={`px-6 py-4 rounded-3xl text-[15px] leading-relaxed shadow-sm ${msg.role === 'user'
                                    ? 'bg-blue-600/10 text-blue-50 border border-blue-500/20 rounded-tr-sm self-end'
                                    : 'bg-slate-800/80 text-slate-200 border border-slate-700/50 rounded-tl-sm'
                                    }`}>
                                    {msg.content}
                                </div>
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex items-start gap-4 max-w-4xl mx-auto animate-pulse">
                            <div className="p-3 rounded-2xl bg-slate-700">
                                <Bot size={20} className="text-blue-400" />
                            </div>
                            <div className="flex flex-col gap-2">
                                <span className="text-[11px] font-bold tracking-widest uppercase text-slate-500">Campus Bot</span>
                                <div className="px-6 py-4 rounded-3xl bg-slate-800 text-slate-400 border border-slate-700 rounded-tl-sm">
                                    Analyzing documents...
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={chatEndRef} />
                </div>

                {/* Input area */}
                <div className="p-10 bg-gradient-to-t from-slate-900 via-slate-900/90 to-transparent">
                    <form
                        onSubmit={handleSend}
                        className="max-w-4xl mx-auto relative group"
                    >
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask about schedule changes, faculty messages, or events..."
                            className="w-full bg-slate-800/50 backdrop-blur-sm border-2 border-slate-700 focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/10 rounded-full py-5 px-8 pr-16 transition-all duration-300 text-lg shadow-2xl placeholder:text-slate-500 placeholder:font-light"
                        />
                        <button
                            type="submit"
                            disabled={loading || !input.trim()}
                            className="absolute right-3 top-3 bottom-3 aspect-square bg-blue-600 hover:bg-blue-500 disabled:opacity-30 text-white rounded-full flex items-center justify-center transition-all duration-300 active:scale-95 shadow-lg shadow-blue-500/40"
                        >
                            <Send size={20} className={loading ? "animate-ping" : ""} />
                        </button>
                    </form>
                    <p className="text-center text-[11px] text-slate-500 mt-6 flex items-center justify-center gap-1.5 opacity-60">
                        <Info size={12} /> Powered by Groq & Llama 3.3 • Vector Retrieval via ChromaDB
                    </p>
                </div>
            </main>
        </div>
    );
}

export default App;
