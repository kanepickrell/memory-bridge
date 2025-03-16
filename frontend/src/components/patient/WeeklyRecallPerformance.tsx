import { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import { Dropdown } from "../ui/dropdown/Dropdown";
import { DropdownItem } from "../ui/dropdown/DropdownItem";
import { MoreDotIcon } from "../../icons";

interface WeeklyPerformanceData {
  weeks: string[];
  srt: number[];
  cst: number[];
  rt: number[];
}

export default function WeeklyRecallPerformance() {
  // State to store fetched weekly performance data
  const [weeklyData, setWeeklyData] = useState<WeeklyPerformanceData>({
    weeks: [],
    srt: [],
    cst: [],
    rt: []
  });

  // Dropdown state
  const [isOpen, setIsOpen] = useState(false);

  // On component mount, fetch data from your API or JSON file
  useEffect(() => {
    // fetch("/data/weekly_performance.json")
    fetch("http://127.0.0.1:8000/weekly_performance")
      .then((res) => res.json())
      .then((data: WeeklyPerformanceData) => {
        setWeeklyData(data);
      })
      .catch((err) => console.error("Error fetching weekly performance:", err));
  }, []);

  function toggleDropdown() {
    setIsOpen(!isOpen);
  }

  function closeDropdown() {
    setIsOpen(false);
  }

  // Chart options
  const options: ApexOptions = {
    colors: ["#465fff", "#00E396", "#FEB019"],
    chart: {
      fontFamily: "Outfit, sans-serif",
      type: "bar",
      height: 180,
      toolbar: { show: false },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "35%",
        borderRadius: 5,
        borderRadiusApplication: "end",
      },
    },
    dataLabels: { enabled: false },
    stroke: {
      show: true,
      width: 2,
      colors: ["transparent"],
    },
    xaxis: {
      categories: weeklyData.weeks,
      axisBorder: { show: false },
      axisTicks: { show: false },
    },
    legend: {
      show: true,
      position: "top",
      horizontalAlign: "left",
      fontFamily: "Outfit",
    },
    yaxis: {
      title: { text: "Accuracy (%)" },
    },
    grid: {
      yaxis: {
        lines: { show: true },
      },
    },
    fill: { opacity: 1 },
    tooltip: {
      x: { show: false },
      y: {
        formatter: (val: number) => `${val}%`,
      },
    },
  };

  // Dynamic series based on fetched data
  const series = [
    { name: "SRT", data: weeklyData.srt },
    { name: "CST", data: weeklyData.cst },
    { name: "RT", data: weeklyData.rt },
  ];

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-5 pt-5 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6 sm:pt-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
          Weekly Recall Performance
        </h3>
        <div className="relative inline-block">
          <button className="dropdown-toggle" onClick={toggleDropdown}>
            <MoreDotIcon className="text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 size-6" />
          </button>
          <Dropdown isOpen={isOpen} onClose={closeDropdown} className="w-40 p-2">
            <DropdownItem
              onItemClick={closeDropdown}
              className="flex w-full font-normal text-left text-gray-500 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
            >
              View More
            </DropdownItem>
            <DropdownItem
              onItemClick={closeDropdown}
              className="flex w-full font-normal text-left text-gray-500 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
            >
              Delete
            </DropdownItem>
          </Dropdown>
        </div>
      </div>

      <div className="max-w-full overflow-x-auto custom-scrollbar">
        <div className="-ml-5 min-w-[650px] xl:min-w-full pl-2">
          <Chart options={options} series={series} type="bar" height={180} />
        </div>
      </div>
    </div>
  );
}
