import React, { useEffect, useState } from 'react';
import { getHistory } from '../api';
import QuizView from './QuizView';
import { Loader2, ArrowRight, ExternalLink, Calendar } from 'lucide-react';

export default function History() {
    const [quizzes, setQuizzes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedQuiz, setSelectedQuiz] = useState(null);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const res = await getHistory();
            setQuizzes(res.data);
        } catch (err) {
            console.error("Failed to load history", err);
        } finally {
            setLoading(false);
        }
    };

    if (selectedQuiz) {
        return (
            <div>
                <button
                    onClick={() => setSelectedQuiz(null)}
                    className="mb-6 flex items-center gap-2 text-gray-500 hover:text-gray-900 transition-colors"
                >
                    &larr; Back to History
                </button>
                <QuizView quizData={selectedQuiz} onReset={() => setSelectedQuiz(null)} />
            </div>
        );
    }

    if (loading) {
        return (
            <div className="flex justify-center items-center py-20">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    if (quizzes.length === 0) {
        return (
            <div className="text-center py-20 text-gray-500">
                <p>No past quizzes found. Generate one!</p>
            </div>
        );
    }

    return (
        <div className="overflow-hidden">
            <table className="w-full text-left border-collapse">
                <thead>
                    <tr className="border-b border-gray-100 text-sm font-semibold text-gray-500 uppercase tracking-wider">
                        <th className="py-4 px-4">Title</th>
                        <th className="py-4 px-4 hidden sm:table-cell">Date</th>
                        <th className="py-4 px-4 text-right">Action</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                    {quizzes.map((quiz) => (
                        <tr key={quiz.id} className="group hover:bg-gray-50 transition-colors">
                            <td className="py-4 px-4">
                                <div className="font-medium text-gray-900">{quiz.title}</div>
                                <a
                                    href={quiz.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-xs text-blue-400 hover:underline flex items-center gap-1 mt-1"
                                    onClick={(e) => e.stopPropagation()}
                                >
                                    <ExternalLink className="w-3 h-3" /> {quiz.url}
                                </a>
                            </td>
                            <td className="py-4 px-4 text-sm text-gray-500 hidden sm:table-cell">
                                <div className="flex items-center gap-2">
                                    <Calendar className="w-4 h-4 text-gray-400" />
                                    {new Date(quiz.created_at).toLocaleDateString()}
                                </div>
                            </td>
                            <td className="py-4 px-4 text-right">
                                <button
                                    onClick={() => setSelectedQuiz(quiz)}
                                    className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-white hover:border-blue-500 hover:text-blue-600 shadow-sm transition-all"
                                >
                                    View Quiz
                                    <ArrowRight className="w-4 h-4" />
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
