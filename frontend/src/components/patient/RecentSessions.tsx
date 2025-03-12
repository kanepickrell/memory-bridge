import {
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
} from "../ui/table";
import { useState } from "react";
import { Dropdown } from "../ui/dropdown/Dropdown";
import { DropdownItem } from "../ui/dropdown/DropdownItem";
import { MoreDotIcon } from "../../icons";

interface Session {
  id: number;
  dateTime: string;       // e.g. "Mar 10, 2025 - 10:00 AM"
  memoryTasks: string;    // e.g. "SRT: 15-word recall"
  notes: string;          // e.g. "85% accuracy; improved from last week"
}

// Example data for recent memory sessions
const sessionData: Session[] = [
  {
    id: 1,
    dateTime: "Mar 10, 2025 - 10:00 AM",
    memoryTasks: "SRT: 15-word recall",
    notes: "85% accuracy; mild improvement from last week.",
  },
  {
    id: 2,
    dateTime: "Mar 12, 2025 - 3:00 PM",
    memoryTasks: "CST: Counting backward from 100 by 7s",
    notes: "No difficulty observed; consider increasing interval for next test.",
  },
  {
    id: 3,
    dateTime: "Mar 15, 2025 - 9:00 AM",
    memoryTasks: "RT: Reaction time with flashcards",
    notes: "Slight delay noted compared to baseline; continue monitoring.",
  },
];

export default function RecentSessions() {
  const [isOpen, setIsOpen] = useState(false);

  function toggleDropdown() {
    setIsOpen(!isOpen);
  }

  function closeDropdown() {
    setIsOpen(false);
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-4 pb-3 pt-4 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6">
      <div className="mb-4 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Recent Memory Sessions
          </h3>
        </div>

        <div className="flex items-center gap-3">
          {/* Dropdown or Filter buttons (optional) */}
          <button
            className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-theme-sm font-medium text-gray-700 shadow-theme-xs 
                       hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 
                       dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
          >
            <svg
              className="stroke-current fill-white dark:fill-gray-800"
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M2.29004 5.90393H17.7067"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M17.7075 14.0961H2.29085"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M12.0826 3.33331C13.5024 3.33331 14.6534 4.48431 14.6534 5.90414C14.6534 7.32398 13.5024 8.47498 12.0826 8.47498C10.6627 8.47498 9.51172 7.32398 9.51172 5.90415C9.51172 4.48432 10.6627 3.33331 12.0826 3.33331Z"
                strokeWidth="1.5"
              />
              <path
                d="M7.91745 11.525C6.49762 11.525 5.34662 12.676 5.34662 14.0959C5.34661 15.5157 6.49762 16.6667 7.91745 16.6667C9.33728 16.6667 10.4883 15.5157 10.4883 14.0959C10.4883 12.676 9.33728 11.525 7.91745 11.525Z"
                strokeWidth="1.5"
              />
            </svg>
            Filter
          </button>
          <button
            className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-theme-sm font-medium text-gray-700 shadow-theme-xs 
                       hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 
                       dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
          >
            See all
          </button>

          {/* Example of a dropdown, if needed */}
          <div className="relative inline-block">
            <button onClick={toggleDropdown}>
              <MoreDotIcon className="size-6 text-gray-400 hover:text-gray-700 dark:hover:text-gray-300" />
            </button>
            <Dropdown isOpen={isOpen} onClose={closeDropdown} className="w-40 p-2">
              <DropdownItem
                onItemClick={closeDropdown}
                className="flex w-full rounded-lg text-left font-normal text-gray-500 hover:bg-gray-100 hover:text-gray-700 
                           dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
              >
                Action 1
              </DropdownItem>
              <DropdownItem
                onItemClick={closeDropdown}
                className="flex w-full rounded-lg text-left font-normal text-gray-500 hover:bg-gray-100 hover:text-gray-700 
                           dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
              >
                Action 2
              </DropdownItem>
            </Dropdown>
          </div>
        </div>
      </div>

      <div className="max-w-full overflow-x-auto">
        <Table>
          {/* Table Header */}
          <TableHeader className="border-y border-gray-100 dark:border-gray-800">
            <TableRow>
              <TableCell
                isHeader
                className="py-3 text-start text-theme-xs font-medium text-gray-500 dark:text-gray-400"
              >
                Date/Time
              </TableCell>
              <TableCell
                isHeader
                className="py-3 text-start text-theme-xs font-medium text-gray-500 dark:text-gray-400"
              >
                Memory Tasks
              </TableCell>
              <TableCell
                isHeader
                className="py-3 text-start text-theme-xs font-medium text-gray-500 dark:text-gray-400"
              >
                Notes
              </TableCell>
            </TableRow>
          </TableHeader>

          {/* Table Body */}
          <TableBody className="divide-y divide-gray-100 dark:divide-gray-800">
            {sessionData.map((session) => (
              <TableRow key={session.id}>
                <TableCell className="py-3 text-gray-800 text-theme-sm dark:text-white/90">
                  {session.dateTime}
                </TableCell>
                <TableCell className="py-3 text-gray-500 text-theme-sm dark:text-gray-400">
                  {session.memoryTasks}
                </TableCell>
                <TableCell className="py-3 text-gray-500 text-theme-sm dark:text-gray-400">
                  {session.notes}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
