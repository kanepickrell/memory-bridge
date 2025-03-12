import WeeklyRecallPerformance from "../../components/patient/WeeklyRecallPerformance";
// import MemoryHealthStatus from "../../components/patient/MemoryHealthStatus";
import LongTermTrends from "../../components/patient/LongTermTrends";
import MonthlyTarget from "../../components/patient/MemoryRecallTarget";
import RecentSessions from "../../components/patient/RecentSessions";
import DemographicCard from "../../components/patient/DemographicCard";
import PageMeta from "../../components/common/PageMeta";

export default function Home() {
  return (
    <>
      <PageMeta
        title="MemoryBridge AI"
        description=""
      />

      {/* Outer wrapper for vertical spacing between rows */}
      <div className="space-y-6">

        {/* Row 1: Memory Health (left) + Memory Recall Target (right) */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {/* <MemoryHealthStatus /> */}
          <WeeklyRecallPerformance />
          <MonthlyTarget />
        </div>

        {/* Row 2: Weekly Recall Performance (left) + Long-term Memory Trends (right) */}
        <div className="grid grid-cols-1 xl:grid-cols-1 gap-6">
          <LongTermTrends />
        </div>

        {/* Row 3: Memory Cluster Map (left) + Recent Memory Sessions (right) */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <DemographicCard />
          <RecentSessions />
        </div>
      </div>
    </>
  );
}
