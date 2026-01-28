import { useState } from 'react'
import QuizGenerator from './components/QuizGenerator'
import History from './components/History'
import { BookOpen, History as HistoryIcon } from 'lucide-react'
import { clsx } from 'clsx'

function App() {
    const [activeTab, setActiveTab] = useState('generate')

    return (
        <div className="min-h-screen bg-gray-100 p-8 font-sans text-gray-800">
            <div className="max-w-5xl mx-auto space-y-6">
                <header className="text-center space-y-2 mb-8">
                    <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
                        AI Wikipedia Quiz Generator
                    </h1>
                    <p className="text-gray-600">Turn any Wikipedia article into an interactive quiz instantly.</p>
                </header>

                <div className="bg-white rounded-2xl shadow-xl overflow-hidden min-h-[600px]">
                    {/* Tabs */}
                    <div className="flex border-b border-gray-100">
                        <button
                            onClick={() => setActiveTab('generate')}
                            className={clsx(
                                "flex-1 py-4 px-6 flex items-center justify-center gap-2 text-sm font-medium transition-colors",
                                activeTab === 'generate'
                                    ? "bg-blue-50 text-blue-600 border-b-2 border-blue-600"
                                    : "text-gray-500 hover:text-gray-700 hover:bg-gray-50"
                            )}
                        >
                            <BookOpen className="w-5 h-5" />
                            Generate Quiz
                        </button>
                        <button
                            onClick={() => setActiveTab('history')}
                            className={clsx(
                                "flex-1 py-4 px-6 flex items-center justify-center gap-2 text-sm font-medium transition-colors",
                                activeTab === 'history'
                                    ? "bg-blue-50 text-blue-600 border-b-2 border-blue-600"
                                    : "text-gray-500 hover:text-gray-700 hover:bg-gray-50"
                            )}
                        >
                            <HistoryIcon className="w-5 h-5" />
                            Past Quizzes
                        </button>
                    </div>

                    {/* Content */}
                    <div className="p-6">
                        {activeTab === 'generate' ? <QuizGenerator /> : <History />}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default App
