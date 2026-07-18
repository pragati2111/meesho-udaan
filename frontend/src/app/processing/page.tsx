"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, Circle, Loader2, XCircle } from "lucide-react";
import { Navbar } from "@/components/shared/Navbar";
import { getAgentIcon } from "@/lib/utils";
import { generateBlueprint } from "@/lib/api/client";
import type { AgentStatus } from "@/lib/types";

const AGENTS = [
  { id: "skill", name: "Skill Discovery Agent", description: "Extracting your core skill and mapping it to market categories" },
  { id: "market", name: "Market Intelligence Agent", description: "Scanning Meesho demand data for your skill category" },
  { id: "trend", name: "Trend Analysis Agent", description: "Identifying seasonal patterns and growth opportunities" },
  { id: "strategy", name: "Business Strategy Agent", description: "Recommending your best product and business model" },
  { id: "pricing", name: "Pricing Agent", description: "Calculating optimal price for maximum margin and sales" },
  { id: "branding", name: "Branding Agent", description: "Creating your brand name, identity, and visual direction" },
  { id: "listing", name: "Listing Generation Agent", description: "Writing your product title, description, and keywords" },
  { id: "growth", name: "Growth Coach Agent", description: "Planning your 90-day launch and growth roadmap" },
];

function StatusIcon({ status }: { status: AgentStatus }) {
  if (status === "completed") return <CheckCircle2 className="h-5 w-5 text-green-500" />;
  if (status === "running") return <Loader2 className="h-5 w-5 animate-spin text-primary" />;
  if (status === "error") return <XCircle className="h-5 w-5 text-destructive" />;
  return <Circle className="h-5 w-5 text-muted-foreground/40" />;
}

export default function ProcessingPage() {
  const router = useRouter();
  const [skillInput, setSkillInput] = useState("");
  const [statuses, setStatuses] = useState<AgentStatus[]>(AGENTS.map(() => "pending"));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const skill = sessionStorage.getItem("skillInput");
    if (!skill) { router.push("/"); return; }
    setSkillInput(skill);
    runPipeline(skill);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const animateAgents = async (onComplete: () => void) => {
    // Animate agents visually while API call runs in parallel
    const delays = [0, 800, 1600, 3000, 4500, 6000, 7500, 9000];
    const durations = [700, 1400, 1200, 1800, 1100, 1600, 1400, 1200];

    for (let i = 0; i < AGENTS.length; i++) {
      await new Promise(r => setTimeout(r, delays[i] - (i > 0 ? delays[i - 1] : 0)));
      setStatuses(prev => prev.map((s, idx) => idx === i ? "running" : s));
      await new Promise(r => setTimeout(r, durations[i]));
      setStatuses(prev => prev.map((s, idx) => idx === i ? "completed" : s));
    }
    onComplete();
  };

  const runPipeline = async (skill: string) => {
    let blueprintId: string | null = null;
    let apiDone = false;

    // Run API call and animation in parallel
    const apiCall = generateBlueprint(skill)
      .then(res => {
        blueprintId = res.blueprintId;
        sessionStorage.setItem("blueprintId", blueprintId);
        apiDone = true;
      })
      .catch(err => {
        setError(err.message || "Something went wrong. Please try again.");
      });

    // Animate regardless of API timing
    await animateAgents(async () => {
      // Wait for API if still running
      await apiCall;
      if (apiDone && blueprintId) {
        router.push(`/dashboard?id=${blueprintId}`);
      } else if (!error) {
        setError("Blueprint generation failed. Please try again.");
      }
    });
  };

  const completed = statuses.filter(s => s === "completed").length;
  const progress = (completed / AGENTS.length) * 100;

  if (error) {
    return (
      <>
        <Navbar />
        <main className="min-h-screen pt-16 flex items-center justify-center">
          <div className="text-center max-w-md px-6">
            <p className="text-2xl mb-2">Something went wrong</p>
            <p className="text-muted-foreground mb-6">{error}</p>
            <button
              onClick={() => router.push("/")}
              className="gradient-bg text-white px-6 py-2 rounded-lg font-medium"
            >
              Try Again
            </button>
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="min-h-screen pt-16">
        <div className="mx-auto max-w-2xl px-6 py-16">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-10 text-center">
            <h1 className="text-3xl font-bold">
              Building your <span className="gradient-text">business blueprint</span>
            </h1>
            <p className="mt-2 text-muted-foreground">&quot;{skillInput}&quot;</p>
            <div className="mt-6 overflow-hidden rounded-full bg-muted h-2">
              <motion.div
                className="h-full rounded-full gradient-bg"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.4, ease: "easeOut" }}
              />
            </div>
            <p className="mt-2 text-sm text-muted-foreground">
              {completed} of {AGENTS.length} agents completed
            </p>
          </motion.div>

          <div className="space-y-3">
            {AGENTS.map((agent, index) => (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.08 }}
                className={`flex items-center gap-4 rounded-xl border p-4 transition-all duration-300 ${
                  statuses[index] === "running"
                    ? "border-primary/30 bg-accent shadow-sm"
                    : statuses[index] === "completed"
                    ? "border-green-500/20 bg-green-500/5"
                    : "border-border/40 bg-card"
                }`}
              >
                <div className="text-xl w-8 text-center">{getAgentIcon(agent.id)}</div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <p className="font-medium text-sm">{agent.name}</p>
                    {statuses[index] === "running" && (
                      <AnimatePresence>
                        <motion.span
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          className="rounded-full gradient-bg px-2 py-0.5 text-xs text-white"
                        >
                          Active
                        </motion.span>
                      </AnimatePresence>
                    )}
                  </div>
                  <p className="text-xs text-muted-foreground mt-0.5 truncate">{agent.description}</p>
                </div>
                <StatusIcon status={statuses[index]} />
              </motion.div>
            ))}
          </div>

          {completed === AGENTS.length && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-8 text-center">
              <p className="gradient-text font-semibold text-lg">✨ Your business blueprint is ready!</p>
              <p className="text-sm text-muted-foreground mt-1">Taking you to your dashboard...</p>
            </motion.div>
          )}
        </div>
      </main>
    </>
  );
}