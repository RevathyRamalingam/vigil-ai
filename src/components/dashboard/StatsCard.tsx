import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  variant?: "default" | "success" | "warning" | "destructive";
}

const variantStyles = {
  default: "border-primary/30 hover:border-primary/50",
  success: "border-success/30 hover:border-success/50",
  warning: "border-warning/30 hover:border-warning/50",
  destructive: "border-destructive/30 hover:border-destructive/50",
};

const iconVariantStyles = {
  default: "text-primary bg-primary/10",
  success: "text-success bg-success/10",
  warning: "text-warning bg-warning/10",
  destructive: "text-destructive bg-destructive/10",
};

export function StatsCard({ title, value, icon: Icon, trend, variant = "default" }: StatsCardProps) {
  return (
    <div className={cn(
      "glass-panel rounded-lg p-6 transition-all duration-300 hover:bg-card/90",
      variantStyles[variant]
    )}>
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <p className="text-3xl font-bold font-mono tracking-tight">{value}</p>
          {trend && (
            <p className={cn(
              "text-xs font-medium",
              trend.isPositive ? "text-success" : "text-destructive"
            )}>
              {trend.isPositive ? "↑" : "↓"} {Math.abs(trend.value)}% from last hour
            </p>
          )}
        </div>
        <div className={cn(
          "p-3 rounded-lg",
          iconVariantStyles[variant]
        )}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
}
