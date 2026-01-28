import React, { useState } from 'react';
import { generateQuiz } from '../api';
import QuizView from './QuizView';
import { Loader2, Search, AlertTriangle } from 'lucide-react';

export default function QuizGenerator() {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [quizData, setQuizData] = useState(null);

    const handleGenerate = async (e) => {
        e.preventDefault();
        if (!url) return;

        setLoading(true);
        setError(null);
        try {
            const res = await generateQuiz(url);
            setQuizData(res.data);
        } catch (err) {
            setError(err.response?.data?.detail || "Failed to generate quiz. Check the URL or try again.");
        } finally {
            setLoading(false);
        }
    };

    if (quizData) {
        return <QuizView quizData={quizData} onReset={() => { setQuizData(null); setUrl(''); }} />;
    }

    return (
        <div className="max-w-xl mx-auto py-12">
            <div className="text-center mb-10">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Generate a New Quiz</h2>
                <p className="text-gray-500">Paste a Wikipedia URL below to generate an AI-powered quiz instantly.</p>
            </div>

            <form onSubmit={handleGenerate} className="space-y-6">
                <div className="relative">
                    <Search className="absolute left-4 top-3.5 text-gray-400 w-5 h-5" />
                    <input
                        type="url"
                        placeholder="https://en.wikipedia.org/wiki/Artificial_intelligence"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        className="w-full pl-12 pr-4 py-3.5 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all text-gray-700 bg-white shadow-sm"
                        required
                    />
                </div>

                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-xl flex items-center gap-3 text-sm animate-in fade-in slide-in-from-top-2">
                        <AlertTriangle className="w-5 h-5 flex-shrink-0" />
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 rounded-xl font-semibold shadow-lg shadow-blue-500/30 hover:shadow-blue-500/40 hover:scale-[1.01] active:scale-[0.99] transition-all disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                    {loading ? (
                        <>
                            <Loader2 className="w-5 h-5 animate-spin" />
                            Analyzing Article & Generating Questions...
                        </>
                    ) : (
                        "Generate Quiz"
                    )}
                </button>
            </form>
        </div>
    );
}
