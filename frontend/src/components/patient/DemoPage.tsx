import React, { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ReactMediaRecorder } from "react-media-recorder";
import chatSound from "./bell.mp3"; // Ensure you have a soft tone sound file

export default function DemoPage() {
    // Session states
    const [sessionActive, setSessionActive] = useState(false);
    const [talking, setTalking] = useState(false);
    const [audioBlobUrl, setAudioBlobUrl] = useState<string | null>(null);

    // We'll store the timestamp when recording starts
    const recordStartRef = useRef<number>(0);

    // Shape variants: morph from rectangle to circle
    const variants = {
        inactive: { width: 400, height: 200, borderRadius: 16 },
        active: { width: 450, height: 450, borderRadius: "50%" },
    };

    // Start session: plays a soft tone, then toggles the "talking" pulse
    const handleStart = () => {
        setSessionActive(true);
        const audio = new Audio(chatSound);
        audio.play();
        setTimeout(() => setTalking(true), 500);
    };

    // End session: stops any talking pulse and resets session states
    const handleEnd = (e: React.MouseEvent) => {
        e.stopPropagation();
        setTalking(false);
        setSessionActive(false);
    };

    // Handle stop recording (ReactMediaRecorder returns a blob URL)
    const handleStop = async (blobUrl: string) => {
        setAudioBlobUrl(blobUrl);
        console.log("Blob URL:", blobUrl);

        // Convert the blob URL into a Blob object
        const res = await fetch(blobUrl);
        const blob = await res.blob();
        console.log("Recorded blob size:", blob.size);

        // If the recording is empty, log an error and do not upload
        if (blob.size === 0) {
            console.error("Recorded audio is empty. Please try again.");
            return;
        }

        // Optional: add a short delay to ensure finalization of the recording
        await new Promise((resolve) => setTimeout(resolve, 300));

        // Send the blob to your backend
        uploadAudio(blob);
    };

    // Upload the audio Blob to the backend
    async function uploadAudio(audioBlob: Blob) {
        const formData = new FormData();
        // The backend expects the field "audio_file"
        formData.append("audio_file", audioBlob, "recording.webm");

        try {
            const response = await fetch("http://127.0.0.1:8000/voice_chat", {
                method: "POST",
                body: formData,
            });

            // Process the MP3 streaming response from the backend
            const audioResponseBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioResponseBlob);
            const audio = new Audio(audioUrl);
            audio.play();
            console.log("Audio response played");
        } catch (error) {
            console.error("Error uploading audio:", error);
        }
    }

    return (
        <div className="fixed inset-0 flex items-center justify-center min-h-screen w-screen bg-white dark:bg-gray-900">
            <motion.div
                className="relative flex items-center justify-center bg-blue-100 dark:bg-gray-800 text-black dark:text-white shadow-md"
                animate={sessionActive ? "active" : "inactive"}
                variants={variants}
                transition={{ duration: 0.5 }}
                onClick={!sessionActive ? handleStart : undefined}
            >
                <AnimatePresence mode="wait">
                    {!sessionActive ? (
                        <motion.div
                            key="start"
                            className="w-full h-full flex items-center justify-center cursor-pointer"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.3 }}
                        >
                            Start Session
                        </motion.div>
                    ) : (
                        <motion.div
                            key="session"
                            className="relative w-full h-full flex flex-col items-center justify-center"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.3 }}
                        >
                            {/* Talking pulse circle */}
                            <motion.div
                                className="w-24 h-24 rounded-full bg-gray-500 dark:bg-gray-600 flex items-center justify-center"
                                animate={{ scale: talking ? [1, 1.2, 1] : 1, opacity: [1, 0.8, 1] }}
                                transition={{ repeat: Infinity, duration: 1 }}
                            />

                            {/* Mute/End Session panel */}
                            <div className="absolute top-5 left-1/2 -translate-x-1/2 flex flex-col bg-white dark:bg-gray-900 text-black dark:text-white p-2 rounded-lg shadow-lg">
                                {/* <button className="flex items-center gap-2 py-1 px-3 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md">
                                    🔇 Mute
                                </button> */}
                                <button
                                    onClick={handleEnd}
                                    className="flex items-center gap-2 text-red-500 py-1 px-3 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
                                >
                                    ⏹ End Session
                                </button>
                            </div>

                            {/* Single large bottom button */}
                            <ReactMediaRecorder
                                audio
                                onStop={handleStop}
                                render={({ status, startRecording, stopRecording }) => (
                                    <div
                                        className="absolute bottom-0 w-full h-16 bg-green-900 rounded-b-[16px] flex items-center justify-center cursor-pointer"
                                        onMouseDown={() => {
                                            recordStartRef.current = Date.now();
                                            startRecording();
                                        }}
                                        onMouseUp={() => {
                                            const duration = Date.now() - recordStartRef.current;
                                            if (duration < 500) {
                                                console.warn("Recording too short, ignoring...");
                                            }
                                            stopRecording();
                                        }}
                                        onMouseLeave={() => {
                                            if (status === "recording") {
                                                stopRecording();
                                            }
                                        }}
                                    >
                                        <span className="text-white text-sm font-medium">
                                            {status === "recording" ? "Recording..." : "Hold to Record"}
                                        </span>
                                    </div>
                                )}
                            />
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.div>
        </div>
    );
}
