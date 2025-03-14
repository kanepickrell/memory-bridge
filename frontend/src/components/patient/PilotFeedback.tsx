// PilotFeedback.jsx
import { useState } from "react";
import PageMeta from "../common/PageMeta";

export default function PilotFeedback() {
    // Placeholder AI responses
    const aiResponses = [
        {
            id: "res1",
            text: "Can you recall any small details, like a window view or a smell?",
        },
        {
            id: "res2",
            text: "Let’s start with something simple—do you remember any sounds or scents from your home?",
        },
        {
            id: "res3",
            text: "I think you should try harder to remember details.",
        },
    ];

    // 1) Track the order in which responses are clicked (for ranking).
    //    e.g., ["res2", "res1", "res3"] => res2 is rank 1, res1 is rank 2, res3 is rank 3.
    const [rankSequence, setRankSequence] = useState([]);

    // 2) Which response is currently selected for editing in the rating form?
    const [selectedResponse, setSelectedResponse] = useState(null);

    // 3) Detailed feedback for each response, keyed by response ID.
    //    Each entry has { ratings: { clarity: x, ... }, feedback: "" }
    const [detailedFeedback, setDetailedFeedback] = useState({
        res1: { ratings: {}, feedback: "" },
        res2: { ratings: {}, feedback: "" },
        res3: { ratings: {}, feedback: "" },
    });

    // Chat state
    const [patientMessage, setPatientMessage] = useState("");
    const [chatHistory, setChatHistory] = useState([]);

    // -------------------------------------
    // RANKING LOGIC
    // -------------------------------------
    // Clicking a response toggles its rank in rankSequence.
    const handleRankClick = (responseId) => {
        setRankSequence((prev) => {
            const index = prev.indexOf(responseId);
            // If it's already in the list, remove it (un-rank).
            if (index !== -1) {
                const newSeq = [...prev];
                newSeq.splice(index, 1);
                return newSeq;
            }
            // Otherwise, if we have room (< 3), add it.
            if (prev.length < 3) {
                return [...prev, responseId];
            }
            // If we already have 3, do nothing or handle differently.
            return prev;
        });
    };

    // Helper to get rank label (1, 2, 3) or null if unranked.
    const getRankLabel = (responseId) => {
        const index = rankSequence.indexOf(responseId);
        return index === -1 ? null : index + 1;
    };

    // Reset all ranks
    const handleResetRanks = () => {
        setRankSequence([]);
    };

    // -------------------------------------
    // DETAILED FEEDBACK LOGIC
    // -------------------------------------
    // Switch the "selected" response for editing
    const handleSelectResponse = (responseId) => {
        setSelectedResponse(responseId);
    };

    // Update a specific rating in the selected response's feedback
    const handleRatingChange = (responseId, category, value) => {
        setDetailedFeedback((prev) => ({
            ...prev,
            [responseId]: {
                ...prev[responseId],
                ratings: {
                    ...prev[responseId].ratings,
                    [category]: value,
                },
            },
        }));
    };

    // Update the textual feedback for the selected response
    const handleTextFeedbackChange = (responseId, value) => {
        setDetailedFeedback((prev) => ({
            ...prev,
            [responseId]: {
                ...prev[responseId],
                feedback: value,
            },
        }));
    };

    // -------------------------------------
    // SUBMIT FEEDBACK
    // -------------------------------------
    const handleSubmitFeedback = async () => {
        // Convert rankSequence into an object: { res1: 1, res2: 2, res3: 3 }
        const ranksObj = rankSequence.reduce((acc, id, i) => {
            acc[id] = i + 1;
            return acc;
        }, {});

        // Build final payload
        const feedbackData = {
            session_id: "session_20250314155454", // Example session ID
            patient_id: "patient_1", // Example patient ID

            // Ranking data
            ranks: ranksObj,

            // Detailed feedback for all responses
            details: detailedFeedback,
        };

        try {
            const response = await fetch("/submit_feedback", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(feedbackData),
            });

            if (response.ok) {
                alert("Feedback submitted successfully!");
                // Reset states
                setRankSequence([]);
                setSelectedResponse(null);
                setDetailedFeedback({
                    res1: { ratings: {}, feedback: "" },
                    res2: { ratings: {}, feedback: "" },
                    res3: { ratings: {}, feedback: "" },
                });
            } else {
                alert("Failed to submit feedback.");
            }
        } catch (error) {
            console.error("Error submitting feedback:", error);
            alert("Error submitting feedback.");
        }
    };

    // -------------------------------------
    // PATIENT CHAT
    // -------------------------------------
    const handlePatientMessageSubmit = async () => {
        if (!patientMessage.trim()) return;

        // Add patient message to chat history
        const newChat = [...chatHistory, { role: "user", content: patientMessage }];
        setChatHistory(newChat);
        setPatientMessage("");

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: patientMessage }),
            });

            const data = await response.json();
            if (data && data.response) {
                setChatHistory((prevChat) => [
                    ...prevChat,
                    { role: "assistant", content: data.response },
                ]);
            }
        } catch (error) {
            console.error("Error getting AI response:", error);
        }
    };

    return (
        <>
            {/* Page Metadata */}
            <PageMeta
                title="Pilot Feedback | MemoryBridge"
                description="Expert feedback for AI memory therapy responses"
            />

            {/* Page Container */}
            <div className="p-4 sm:p-6 lg:p-8 space-y-6 bg-white dark:bg-gray-900 min-h-screen text-gray-800 dark:text-gray-100">
                {/* Page Header */}
                <div className="space-y-1">
                    <h1 className="text-2xl font-bold">
                        Pilot Feedback
                    </h1>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                        1) Click each response in order of preference to rank them (1–3).
                        2) Enter detailed ratings for each response (optional).
                        3) Submit your final feedback below.
                    </p>
                </div>

                {/* AI Responses + Ranking Section */}
                <div className="flex flex-col md:flex-row gap-4">
                    {aiResponses.map((res) => {
                        const rankLabel = getRankLabel(res.id);
                        const { ratings, feedback } = detailedFeedback[res.id];
                        const isSelected = selectedResponse === res.id;

                        return (
                            <div
                                key={res.id}
                                className="flex-1 rounded-lg border border-gray-200 
                                           dark:border-gray-700 bg-white dark:bg-gray-800 p-4 shadow-sm 
                                           hover:shadow-md transition-shadow relative space-y-2"
                            >
                                <p className="text-sm md:text-base">{res.text}</p>

                                {/* Rank Display / Toggle */}
                                <button
                                    className={`inline-block px-3 py-1 text-sm rounded-full 
                                                border dark:border-gray-600
                                                ${rankLabel
                                            ? "bg-green-100 dark:bg-green-700/50 text-green-700 dark:text-green-100"
                                            : "bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-200"
                                        }`}
                                    onClick={() => handleRankClick(res.id)}
                                >
                                    {rankLabel
                                        ? `Rank: ${rankLabel}`
                                        : "Click to Rank"}
                                </button>

                                {/* Expand / Collapse Detailed Ratings */}
                                <button
                                    className={`block w-full bg-blue-100 dark:bg-blue-700/50 
                                                text-blue-600 dark:text-blue-200 p-2 rounded-lg 
                                                hover:bg-blue-200 dark:hover:bg-blue-700 text-sm font-medium
                                                ${isSelected ? "ring-2 ring-blue-500" : ""}`}
                                    onClick={() => handleSelectResponse(isSelected ? null : res.id)}
                                >
                                    {isSelected ? "Hide Ratings" : "Show Ratings"}
                                </button>

                                {/* Detailed Ratings for This Response (inline) */}
                                {isSelected && (
                                    <div className="mt-2 bg-gray-50 dark:bg-gray-700 p-3 rounded space-y-2">
                                        <p className="text-xs italic text-gray-600 dark:text-gray-200">
                                            Detailed Feedback for: "{res.text}"
                                        </p>

                                        {/* Ratings Grid */}
                                        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                                            {["clarity", "therapeutic_value", "empathy", "personalization", "consistency", "safety"].map(
                                                (category) => (
                                                    <div key={category} className="flex flex-col space-y-1">
                                                        <label className="text-xs font-medium capitalize">
                                                            {category.replace("_", " ")}
                                                        </label>
                                                        <select
                                                            className="border dark:border-gray-600 rounded p-1 bg-white dark:bg-gray-900 text-xs"
                                                            value={ratings[category] || ""}
                                                            onChange={(e) =>
                                                                handleRatingChange(res.id, category, Number(e.target.value))
                                                            }
                                                        >
                                                            <option value="">--</option>
                                                            {[1, 2, 3, 4, 5].map((num) => (
                                                                <option key={num} value={num}>
                                                                    {num}
                                                                </option>
                                                            ))}
                                                        </select>
                                                    </div>
                                                )
                                            )}
                                        </div>

                                        {/* Qualitative Feedback Input */}
                                        <textarea
                                            className="w-full p-2 border dark:border-gray-600 rounded bg-white dark:bg-gray-900 text-sm"
                                            placeholder="Provide additional feedback..."
                                            value={feedback}
                                            onChange={(e) => handleTextFeedbackChange(res.id, e.target.value)}
                                        />
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>

                {/* Reset Ranks Button */}
                <div className="flex justify-end">
                    <button
                        className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 px-4 py-2 rounded 
                                   hover:bg-gray-300 dark:hover:bg-gray-600 text-sm"
                        onClick={handleResetRanks}
                    >
                        Reset Ranks
                    </button>
                </div>

                {/* Submit All Feedback */}
                <button
                    onClick={handleSubmitFeedback}
                    className="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 text-sm font-medium"
                >
                    Submit Feedback
                </button>

                {/* Patient Chatbox Section */}
                <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg shadow space-y-4">
                    <h2 className="text-lg font-semibold">Patient-AI Chat</h2>

                    {/* Chat History */}
                    <div className="h-48 overflow-y-auto border dark:border-gray-700 p-2 rounded bg-white dark:bg-gray-900 space-y-2 text-sm">
                        {chatHistory.map((msg, index) => (
                            <div
                                key={index}
                                className={
                                    msg.role === "user"
                                        ? "text-right text-blue-600 dark:text-blue-400"
                                        : "text-left text-gray-800 dark:text-gray-100"
                                }
                            >
                                <strong>{msg.role === "user" ? "Patient: " : "AI: "}</strong> {msg.content}
                            </div>
                        ))}
                    </div>

                    {/* Chat Input */}
                    <div className="flex space-x-2">
                        <input
                            type="text"
                            className="flex-1 border dark:border-gray-700 p-2 rounded bg-white dark:bg-gray-900 text-sm"
                            placeholder="Type message..."
                            value={patientMessage}
                            onChange={(e) => setPatientMessage(e.target.value)}
                        />
                        <button
                            onClick={handlePatientMessageSubmit}
                            className="bg-green-500 text-white px-4 rounded hover:bg-green-600 text-sm font-medium"
                        >
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
}
