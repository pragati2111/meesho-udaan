"use client";

import Link from "next/link";
import { Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border/40 bg-background/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="gradient-bg flex h-8 w-8 items-center justify-center rounded-lg">
            <Sparkles className="h-4 w-4 text-white" />
          </div>
          <span className="text-lg font-bold">
            Meesho <span className="gradient-text">Udaan</span>
          </span>
        </Link>

        <div className="flex items-center gap-3">
          <span className="hidden text-sm text-muted-foreground sm:block">
            The Entrepreneur Discovery Engine
          </span>
          <Button size="sm" className="gradient-bg text-white border-0 hover:opacity-90">
            Get Started
          </Button>
        </div>
      </div>
    </nav>
  );
}