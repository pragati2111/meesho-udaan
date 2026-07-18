import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getAgentIcon(agentId: string): string {
  switch (agentId) {
    case "skill":
      return "🧠";
    case "market":
      return "📈";
    case "trend":
      return "📊";
    case "strategy":
      return "🎯";
    case "pricing":
      return "💰";
    case "branding":
      return "🎨";
    case "listing":
      return "📝";
    case "growth":
      return "🚀";
    default:
      return "🤖";
  }
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(amount);
}