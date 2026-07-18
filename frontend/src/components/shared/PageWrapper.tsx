import { cn } from "@/lib/utils";

interface PageWrapperProps {
  children: React.ReactNode;
  className?: string;
}

export function PageWrapper({ children, className }: PageWrapperProps) {
  return (
    <main
      className={cn(
        "min-h-screen pt-16",
        className
      )}
    >
      {children}
    </main>
  );
}