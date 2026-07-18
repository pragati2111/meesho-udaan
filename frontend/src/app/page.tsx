"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  Sparkles,
  Mic,
  Camera,
  Type,
  ArrowRight,
  Zap,
  TrendingUp,
  Star,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Navbar } from "@/components/shared/Navbar";

type InputMode = "text" | "voice" | "image";

const EXAMPLE_SKILLS = [
  "I stitch and embroider traditional Rajasthani suits",
  "I make handmade jewellery using terracotta and clay",
  "I bake cakes and Indian mithai for weddings and events",
  "I weave Banarasi silk sarees on a handloom",
  "I make pickles, murabbas, and chutneys at home",
  "I do block printing on fabric using natural dyes",
];

const STATS = [
  { icon: Zap, label: "Seconds to a business plan", value: "< 60" },
  { icon: TrendingUp, label: "Market demand validated", value: "Real-time" },
  { icon: Star, label: "Entrepreneurs discovered", value: "1M+" },
];

export default function HomePage() {
  const router = useRouter();
  const [inputMode, setInputMode] = useState<InputMode>("text");
  const [skillText, setSkillText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleExampleClick = (example: string) => {
    setSkillText(example);
    setInputMode("text");
  };

  const handleSubmit = async () => {
  if (!skillText.trim()) return;
  setIsLoading(true);

  try {
    sessionStorage.setItem("skillInput", skillText);
    router.push("/processing");
  } catch {
    setIsLoading(false);
  }
};

  return (
    <>
      <Navbar />

      <main className="min-h-screen pt-16">
        {/* Hero Section */}
        <section className="relative overflow-hidden">
          {/* Background decoration */}
          <div className="pointer-events-none absolute inset-0 overflow-hidden">
            <div
              className="absolute -top-40 -right-40 h-96 w-96 rounded-full opacity-10 blur-3xl"
              style={{ background: "var(--meesho-gradient-from)" }}
            />
            <div
              className="absolute top-20 -left-40 h-80 w-80 rounded-full opacity-8 blur-3xl"
              style={{ background: "var(--meesho-gradient-to)" }}
            />
          </div>

          <div className="relative mx-auto max-w-4xl px-6 py-20 text-center">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-accent px-4 py-1.5 text-sm font-medium text-accent-foreground"
            >
              <Sparkles className="h-3.5 w-3.5" />
              Powered by Agentic AI · Built for Bharat
            </motion.div>

            {/* Headline */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-5xl font-bold tracking-tight sm:text-6xl lg:text-7xl"
            >
              What are you{" "}
              <span className="gradient-text">already good at?</span>
            </motion.h1>

            {/* Subheadline */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mt-6 text-lg text-muted-foreground sm:text-xl max-w-2xl mx-auto leading-relaxed"
            >
              Tell us your skill. Our AI agents will discover your business
              opportunity, build your brand, price your products, and create
              your Meesho store — in under 60 seconds.
            </motion.p>

            {/* Input Card */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="mt-10 rounded-2xl border border-border/60 bg-card p-6 shadow-xl text-left"
            >
              {/* Input Mode Selector */}
              <div className="mb-4 flex gap-2">
                {(["text", "voice", "image"] as InputMode[]).map((mode) => (
                  <button
                    key={mode}
                    onClick={() => setInputMode(mode)}
                    className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-all ${
                      inputMode === mode
                        ? "gradient-bg text-white shadow-sm"
                        : "bg-muted text-muted-foreground hover:bg-secondary"
                    }`}
                  >
                    {mode === "text" && <Type className="h-3.5 w-3.5" />}
                    {mode === "voice" && <Mic className="h-3.5 w-3.5" />}
                    {mode === "image" && <Camera className="h-3.5 w-3.5" />}
                    {mode.charAt(0).toUpperCase() + mode.slice(1)}
                  </button>
                ))}
              </div>

              {/* Input Area */}
              <AnimatePresence mode="wait">
                {inputMode === "text" && (
                  <motion.div
                    key="text"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                  >
                    <Textarea
                      placeholder="Describe your skill... e.g. I stitch school uniforms and do block printing on fabric"
                      value={skillText}
                      onChange={(e) => setSkillText(e.target.value)}
                      className="min-h-[120px] resize-none border-0 bg-muted/50 text-base focus-visible:ring-1 focus-visible:ring-primary"
                    />
                  </motion.div>
                )}

                {inputMode === "voice" && (
                  <motion.div
                    key="voice"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="flex min-h-[120px] flex-col items-center justify-center gap-3 rounded-lg bg-muted/50"
                  >
                    <div className="gradient-bg flex h-14 w-14 items-center justify-center rounded-full shadow-lg">
                      <Mic className="h-6 w-6 text-white" />
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Voice input coming in Phase 7
                    </p>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setInputMode("text")}
                    >
                      Use text instead
                    </Button>
                  </motion.div>
                )}

                {inputMode === "image" && (
                  <motion.div
                    key="image"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="flex min-h-[120px] flex-col items-center justify-center gap-3 rounded-lg bg-muted/50"
                  >
                    <div className="gradient-bg flex h-14 w-14 items-center justify-center rounded-full shadow-lg">
                      <Camera className="h-6 w-6 text-white" />
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Image input coming in Phase 8
                    </p>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setInputMode("text")}
                    >
                      Use text instead
                    </Button>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Submit Button */}
              <Button
                onClick={handleSubmit}
                disabled={!skillText.trim() || isLoading}
                className="mt-4 w-full gradient-bg border-0 text-white hover:opacity-90 h-12 text-base font-semibold"
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                    Discovering your business...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    Discover My Business
                    <ArrowRight className="h-4 w-4" />
                  </span>
                )}
              </Button>
            </motion.div>

            {/* Example Skills */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="mt-6"
            >
              <p className="mb-3 text-sm text-muted-foreground">
                Try an example:
              </p>
              <div className="flex flex-wrap justify-center gap-2">
                {EXAMPLE_SKILLS.map((skill) => (
                  <button
                    key={skill}
                    onClick={() => handleExampleClick(skill)}
                    className="rounded-full border border-border/60 bg-card px-3 py-1.5 text-xs text-muted-foreground transition-all hover:border-primary/40 hover:text-foreground hover:shadow-sm"
                  >
                    {skill}
                  </button>
                ))}
              </div>
            </motion.div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="border-t border-border/40 bg-muted/30">
          <div className="mx-auto max-w-4xl px-6 py-12">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
              {STATS.map((stat) => (
                <div key={stat.label} className="text-center">
                  <div className="gradient-bg mx-auto mb-3 flex h-10 w-10 items-center justify-center rounded-xl">
                    <stat.icon className="h-5 w-5 text-white" />
                  </div>
                  <div className="text-2xl font-bold gradient-text">
                    {stat.value}
                  </div>
                  <div className="mt-1 text-sm text-muted-foreground">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How it works */}
        <section className="mx-auto max-w-4xl px-6 py-16">
          <h2 className="mb-2 text-center text-3xl font-bold">
            How Udaan works
          </h2>
          <p className="mb-10 text-center text-muted-foreground">
            Eight specialized AI agents work together — so you don&apos;t have
            to.
          </p>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                icon: "🎯",
                title: "Skill Discovery",
                desc: "Extracts what you're good at and maps it to sellable products",
              },
              {
                icon: "📊",
                title: "Market Intelligence",
                desc: "Validates demand in real-time across Meesho categories",
              },
              {
                icon: "💰",
                title: "Pricing Strategy",
                desc: "Calculates the price that maximizes your margin and sales",
              },
              {
                icon: "✨",
                title: "Brand & Listings",
                desc: "Creates your store name, identity, and product copy",
              },
            ].map((step) => (
              <div
                key={step.title}
                className="rounded-xl border border-border/60 bg-card p-5 transition-shadow hover:shadow-md"
              >
                <div className="mb-3 text-2xl">{step.icon}</div>
                <h3 className="mb-1.5 font-semibold">{step.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {step.desc}
                </p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </>
  );
}