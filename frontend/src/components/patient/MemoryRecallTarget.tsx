import { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import { Dropdown } from "../ui/dropdown/Dropdown";
import { DropdownItem } from "../ui/dropdown/DropdownItem";
import { MoreDotIcon } from "../../icons";

// The structure of your weekly data JSON
interface WeeklyPerformanceData {
  weeks: string[];
  srt: number[];
  cst: number[];
  rt: number[];
}

export default function MemoryRecallTarget() {
  const [recallAccuracy, setRecallAccuracy] = useState<number>(0);
  const recallTarget = 90;

  const [isOpen, setIsOpen] = useState(false);
  function toggleDropdown() {
    setIsOpen(!isOpen);
  }
  function closeDropdown() {
    setIsOpen(false);
  }

  useEffect(() => {
    fetch("http://127.0.0.1:8000/weekly_performance")
      .then((res) => res.json())
      .then((data: WeeklyPerformanceData) => {
        const totalWeeks = data.weeks.length;
        if (totalWeeks === 0) return;

        const sumSrt = data.srt.reduce((a, b) => a + b, 0);
        const sumCst = data.cst.reduce((a, b) => a + b, 0);
        const sumRt = data.rt.reduce((a, b) => a + b, 0);

        const totalSum = sumSrt + sumCst + sumRt;
        const totalDataPoints = totalWeeks * 3; // srt, cst, rt
        const overallAvg = totalSum / totalDataPoints;

        setRecallAccuracy(Math.round(overallAvg));
      })
      .catch((err) => console.error("Error fetching weekly performance:", err));
  }, []);

  const series = [recallAccuracy];

  // Remove the `formatter` property from the `name` object
  // and use `labels: ["Recall Accuracy"]` below
  const options: ApexOptions = {
    chart: {
      fontFamily: "Outfit, sans-serif",
      type: "radialBar",
      height: 330,
      sparkline: { enabled: true },
    },
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        hollow: { size: "70%" },
        track: {
          background: "#E4E7EC",
          strokeWidth: "100%",
          margin: 5,
        },
        dataLabels: {
          name: {
            show: true,
            fontSize: "14px",
            color: "#1D2939",
            offsetY: 10,
            // Removed formatter here
          },
          value: {
            fontSize: "36px",
            fontWeight: "600",
            color: "#1D2939",
            offsetY: -15,
            formatter: (val: number) => `${val}%`,
          },
        },
      },
    },
    colors: ["#465FFF"],
    stroke: { lineCap: "round" },
    labels: ["Recall Accuracy"], // This sets the name label
  };

  return (
    <div className="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
      <div className="px-5 pt-5 bg-white shadow-default rounded-2xl pb-5 dark:bg-gray-900 sm:px-6 sm:pt-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
              Memory Recall Target
            </h3>
            <p className="mt-1 text-gray-500 text-theme-sm dark:text-gray-400">
              Target recall accuracy for memory tests.
            </p>
          </div>
          <div className="relative inline-block">
            <button className="dropdown-toggle" onClick={toggleDropdown}>
              <MoreDotIcon className="text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 size-6" />
            </button>
            <Dropdown isOpen={isOpen} onClose={closeDropdown} className="w-40 p-2">
              <DropdownItem
                onItemClick={closeDropdown}
                className="flex w-full font-normal text-left text-gray-500 rounded-lg
                           hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 
                           dark:hover:bg-white/5 dark:hover:text-gray-300"
              >
                View More
              </DropdownItem>
              <DropdownItem
                onItemClick={closeDropdown}
                className="flex w-full font-normal text-left text-gray-500 rounded-lg 
                           hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 
                           dark:hover:bg-white/5 dark:hover:text-gray-300"
              >
                Delete
              </DropdownItem>
            </Dropdown>
          </div>
        </div>

        <div className="relative">
          <Chart options={options} series={series} type="radialBar" height={330} />
        </div>

        <div className="mt-5 text-center">
          <p className="text-sm text-gray-500">
            Target Recall Accuracy: {recallTarget}%
          </p>
        </div>
      </div>
    </div>
  );
}
