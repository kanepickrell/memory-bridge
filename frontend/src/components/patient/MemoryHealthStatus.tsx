// import React from "react";

export default function MemoryHealthStatus() {
    // Example: current recall accuracy
    const recallAccuracy = 82;
    // Example: target recall accuracy
    const recallTarget = 85;

    // Decide memory health status
    let memoryHealthStatus = "Stable";
    let bgColor = "bg-green-500";

    if (recallAccuracy < 70) {
        memoryHealthStatus = "Immediate Attention";
        bgColor = "bg-red-500";
    } else if (recallAccuracy < recallTarget) {
        memoryHealthStatus = "Mild Concern";
        bgColor = "bg-yellow-400";
    }

    return (
        <div className="rounded-xl border p-4 flex items-center justify-between bg-white dark:bg-white/[0.03] dark:border-gray-800">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Memory Health
            </p>
            <div className="flex items-center gap-2">
                {/* A small circle as a "traffic light" indicator */}
                <span className={`h-4 w-4 rounded-full ${bgColor}`} />
                <p className="text-sm font-semibold text-gray-800 dark:text-gray-100">
                    {memoryHealthStatus}
                </p>
            </div>
        </div>
    );
}
