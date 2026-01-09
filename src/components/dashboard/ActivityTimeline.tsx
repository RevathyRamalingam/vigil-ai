import { cn } from "@/lib/utils";
import { Scan, ShieldCheck, AlertTriangle, Camera } from "lucide-react";
import { LucideIcon } from "lucide-react";

type ActivityType = "scan" | "clear" | "alert" | "camera";

interface Activity {
  id: string;
  type: ActivityType;
  message: string;
  timestamp: string;
}

interface ActivityTimelineProps {
  activities: Activity[];
}

const typeConfig: Record<ActivityType, { icon: LucideIcon; className: string }> = {
  scan: {
    icon: Scan,
    className: "text-primary bg-primary/10 border-primary/30",
  },
  clear: {
    icon: ShieldCheck,
    className: "text-success bg-success/10 border-success/30",
  },
  alert: {
    icon: AlertTriangle,
    className: "text-destructive bg-destructive/10 border-destructive/30",
  },
  camera: {
    icon: Camera,
    className: "text-muted-foreground bg-muted border-border",
  },
};

export function ActivityTimeline({ activities }: ActivityTimelineProps) {
  return (
    <div className="glass-panel rounded-lg p-4">
      <h3 className="font-semibold mb-4 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-primary status-pulse" />
        Live Activity
      </h3>
      
      <div className="space-y-3 max-h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-muted scrollbar-track-transparent">
        {activities.map((activity, index) => {
          const config = typeConfig[activity.type];
          const Icon = config.icon;
          
          return (
            <div 
              key={activity.id} 
              className="flex items-start gap-3 animate-fade-in"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className="relative">
                <div className={cn(
                  "p-1.5 rounded-full border",
                  config.className
                )}>
                  <Icon className="w-3 h-3" />
                </div>
                {index < activities.length - 1 && (
                  <div className="absolute left-1/2 top-full w-px h-3 -translate-x-1/2 bg-border" />
                )}
              </div>
              
              <div className="flex-1 min-w-0 pt-0.5">
                <p className="text-sm">{activity.message}</p>
                <p className="text-xs text-muted-foreground font-mono mt-0.5">{activity.timestamp}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
