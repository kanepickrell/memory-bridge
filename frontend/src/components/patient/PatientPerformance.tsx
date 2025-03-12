// import React from "react";
import PageMeta from "../../components/common/PageMeta";
import MemoryHealthStatus from "../../components/patient/MemoryHealthStatus";
import WeeklyRecallPerformance from "../../components/patient/WeeklyRecallPerformance";
import MemoryRecallTarget from "../../components/patient/MemoryRecallTarget";
import StatisticsChart from "../../components/patient/LongTermTrends";
import DemographicCard from "../../components/patient/DemographicCard";
import RecentSessions from "../../components/patient/RecentSessions";

export default function PatientPerformance() {
    return (
        <>
            <PageMeta
                title="Patient Performance | MemoryBridge"
                description="Detailed metrics and insights for patient memory performance."
            />

            {/* Page Container */}
            <div className="p-4 sm:p-6 lg:p-8 space-y-6">
                {/* Page Heading */}
                <div>
                    <h1 className="text-2xl font-bold text-gray-800 dark:text-white/90">
                        Patient Performance
                    </h1>
                    <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                        All key memory metrics and insights in one place.
                    </p>
                </div>

                {/* Row 1: Memory Health + Recall Target */}
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                    <MemoryHealthStatus />
                    <MemoryRecallTarget />
                </div>

                {/* Row 2: Weekly Performance + Long-Term Trends */}
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                    <WeeklyRecallPerformance />
                    <StatisticsChart />
                </div>

                {/* Row 3: Memory Cluster Map + Recent Sessions */}
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                    <DemographicCard />
                    <RecentSessions />
                </div>
            </div>
        </>
    );
}
