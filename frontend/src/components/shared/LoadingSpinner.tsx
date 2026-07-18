import { cn } from "@/lib/utils";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizes = {
  sm: "h-4 w-4 border-2",
  md: "h-8 w-8 border-2",
  lg: "h-12 w-12 border-3",
};

export function LoadingSpinner({ size = "md", className }: LoadingSpinnerProps) {
  return (
    <div
      className={cn(
        "animate-spin rounded-full border-transparent",
        "border-t-primary border-r-primary",
        sizes[size],
        className
      )}
      style={{ borderTopColor: "var(--meesho-gradient-from)", borderRightColor: "var(--meesho-gradient-from)" }}
    />
  );
}