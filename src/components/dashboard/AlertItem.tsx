import { cn } from "@/lib/utils";
import { AlertTriangle, ShieldAlert, User, Car, Clock } from "lucide-react";
import { LucideIcon } from "lucide-react";

type AlertSeverity = "high" | "medium" | "low";
type AlertType = "intrusion" | "suspicious_person" | "vehicle" | "general";

interface AlertItemProps {
  id: string;
  type: AlertType;
  severity: AlertSeverity;
  title: string;
  location: string;
  timestamp: string;
  cameraId: string;
}

const severityConfig = {
  high: {
    className: "border-l-destructive bg-destructive/5",
    badge: "bg-destructive/20 text-destructive border-destructive/30",
    label: "High",
  },
  medium: {
    className: "border-l-warning bg-warning/5",
    badge: "bg-warning/20 text-warning border-warning/30",
    label: "Medium",
  },
  low: {
    className: "border-l-primary bg-primary/5",
    badge: "bg-primary/20 text-primary border-primary/30",
    label: "Low",
  },
};

const typeIcons: Record<AlertType, LucideIcon> = {
  intrusion: ShieldAlert,
  suspicious_person: User,
  vehicle: Car,
  general: AlertTriangle,
};

export function AlertItem({ id, type, severity, title, location, timestamp, cameraId }: AlertItemProps) {
  const config = severityConfig[severity];
  const TypeIcon = typeIcons[type];

  return (
    <div className={cn(
      "glass-panel rounded-lg p-4 border-l-4 animate-fade-in cursor-pointer hover:bg-card/90 transition-colors",
      config.className
    )}>
      <div className="flex items-start gap-3">
        <div className={cn(
          "p-2 rounded-lg",
          severity === "high" ? "bg-destructive/10 text-destructive" :
          severity === "medium" ? "bg-warning/10 text-warning" :
          "bg-primary/10 text-primary"
        )}>
          <TypeIcon className="w-4 h-4" />
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <h4 className="font-medium text-sm truncate">{title}</h4>
            <span className={cn(
              "px-2 py-0.5 rounded-full text-[10px] font-medium border shrink-0",
              config.badge
            )}>
              {config.label}
            </span>
          </div>
          
          <p className="text-xs text-muted-foreground mb-2">{location}</p>
          
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {timestamp}
            </span>
            <span className="font-mono text-primary">{cameraId}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
