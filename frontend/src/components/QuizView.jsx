import React, { useState } from 'react';
import { CheckCircle2, XCircle, Sparkles } from 'lucide-react';
import { clsx } from 'clsx';

const DifficultyBadge = ({ level }) => {
    const colors = {
        easy: 'bg-green-100 text-green-700',
        medium: 'bg-yellow-100 text-yellow-700',
        hard: 'bg-red-100 text-red-700'
    };
    return (
        <span className={clsx("px-2 py-1 rounded-full text-xs font-semibold uppercase tracking-wider", colors[level.toLowerCase()] || colors.medium)}>
            {level}
        </span>
    );
};

export default function QuizView({ quizData, onReset }) {
    const [userAnswers, setUserAnswers] = useState({});
    const [submitted, setSubmitted] = useState(false);
    const [score, setScore] = useState(0);

    const handleSelect = (qIndex, option) => {
        if (submitted) return;
        setUserAnswers(prev => ({
            ...prev,
            [qIndex]: option
        }));
    };

    const handleSubmit = () => {
        let newScore = 0;
        quizData.quiz.forEach((q, idx) => {
            if (userAnswers[idx] === q.answer) {
                newScore++;
            }
        });
        setScore(newScore);
        setSubmitted(true);
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="space-y-4 border-b pb-6">
                <div className="flex justify-between items-start">
                    <h2 className="text-2xl font-bold text-gray-800">{quizData.title}</h2>
                    <a href={quizData.url} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-500 hover:underline">
                        View Article
                    </a>
                </div>
                <p className="text-gray-600 leading-relaxed">{quizData.summary}</p>
                <div className="flex flex-wrap gap-2">
                    {quizData.related_topics && quizData.related_topics.map((topic, i) => (
                        <span key={i} className="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs border border-gray-200">
                            {topic}
                        </span>
                    ))}
                </div>


            </div>

            <div className="space-y-8">
                {quizData.quiz.map((q, idx) => {
                    const isCorrect = userAnswers[idx] === q.answer;
                    const isWrong = submitted && userAnswers[idx] !== q.answer;

                    return (
                        <div key={idx} className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
                            <div className="flex justify-between items-center mb-4">
                                <span className="text-sm font-medium text-gray-500">Question {idx + 1}</span>
                                <DifficultyBadge level={q.difficulty} />
                            </div>
                            <h3 className="text-lg font-medium text-gray-900 mb-6">{q.question}</h3>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {Object.entries(q.options).map(([key, value]) => {
                                    const isSelected = userAnswers[idx] === key;
                                    let btnClass = "border-gray-200 hover:bg-gray-50 hover:border-gray-300";

                                    if (submitted) {
                                        if (key === q.answer) btnClass = "bg-green-50 border-green-500 text-green-700 font-medium";
                                        else if (isSelected && key !== q.answer) btnClass = "bg-red-50 border-red-500 text-red-700";
                                    } else {
                                        if (isSelected) btnClass = "bg-blue-50 border-blue-500 text-blue-700 ring-1 ring-blue-500";
                                    }

                                    return (
                                        <button
                                            key={key}
                                            onClick={() => handleSelect(idx, key)}
                                            disabled={submitted}
                                            className={clsx(
                                                "w-full text-left p-4 rounded-lg border transition-all duration-200 flex items-center justify-between group",
                                                btnClass
                                            )}
                                        >
                                            <span className="flex items-center gap-3">
                                                <span className={clsx(
                                                    "w-6 h-6 rounded-full flex items-center justify-center text-xs border",
                                                    submitted && key === q.answer ? "bg-green-500 text-white border-green-500" :
                                                        submitted && isSelected && key !== q.answer ? "bg-red-500 text-white border-red-500" :
                                                            isSelected ? "bg-blue-500 text-white border-blue-500" : "bg-gray-100 text-gray-500 border-gray-300"
                                                )}>
                                                    {key}
                                                </span>
                                                {value}
                                            </span>
                                            {submitted && key === q.answer && <CheckCircle2 className="w-5 h-5 text-green-600" />}
                                            {submitted && isSelected && key !== q.answer && <XCircle className="w-5 h-5 text-red-500" />}
                                        </button>
                                    );
                                })}
                            </div>

                            {submitted && (
                                <div className="mt-6 p-4 bg-blue-50 rounded-lg flex items-start gap-3 text-sm text-blue-800">
                                    <Sparkles className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                    <div>
                                        <span className="font-semibold block mb-1">Explanation:</span>
                                        {q.explanation}
                                    </div>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>

            {!submitted ? (
                <div className="flex justify-end pt-6">
                    <button
                        onClick={handleSubmit}
                        disabled={Object.keys(userAnswers).length !== quizData.quiz.length}
                        className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-3 rounded-xl font-semibold shadow-lg shadow-blue-500/30 hover:shadow-blue-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Submit Quiz
                    </button>
                </div>
            ) : (
                <div className="bg-gray-900 text-white p-6 rounded-2xl flex items-center justify-between shadow-2xl">
                    <div>
                        <p className="text-gray-400 text-sm uppercase tracking-wide font-medium">Your Score</p>
                        <p className="text-4xl font-bold mt-1">
                            {score} <span className="text-2xl text-gray-500 font-normal">/ {quizData.quiz.length}</span>
                        </p>
                    </div>
                    <button
                        onClick={onReset}
                        className="bg-white text-gray-900 px-6 py-2.5 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                    >
                        Generate Another
                    </button>
                </div>
            )}
        </div>
    );
}
