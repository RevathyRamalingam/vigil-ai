import { cn } from "@/lib/utils";
import { AlertTriangle, CheckCircle, Video, Maximize2 } from "lucide-react";

interface CameraFeedProps {
  id: string;
  name: string;
  location: string;
  status: "online" | "offline" | "alert";
  lastAlert?: string;
  imageUrl?: string;
}

const statusConfig = {
  online: {
    label: "Online",
    icon: CheckCircle,
    className: "text-success bg-success/20 border-success/30",
    dotClass: "bg-success",
  },
  offline: {
    label: "Offline",
    icon: Video,
    className: "text-muted-foreground bg-muted border-border",
    dotClass: "bg-muted-foreground",
  },
  alert: {
    label: "Alert",
    icon: AlertTriangle,
    className: "text-destructive bg-destructive/20 border-destructive/30",
    dotClass: "bg-destructive",
  },
};

export function CameraFeed({ id, name, location, status, lastAlert, imageUrl }: CameraFeedProps) {
  const config = statusConfig[status];
  const StatusIcon = config.icon;

  return (
    <div className={cn(
      "glass-panel rounded-lg overflow-hidden group transition-all duration-300",
      status === "alert" && "border-destructive/50 glow-destructive"
    )}>
      <div className="relative aspect-video bg-muted/30 overflow-hidden">
        {imageUrl ? (
          <img 
            src={imageUrl} 
            alt={`Camera feed: ${name}`}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Video className="w-12 h-12 text-muted-foreground/50" />
          </div>
        )}
        
        {/* Scan line effect for active cameras */}
        {status === "online" && (
          <div className="absolute inset-0 overflow-hidden pointer-events-none">
            <div className="absolute w-full h-1 bg-gradient-to-r from-transparent via-primary/30 to-transparent scan-line" />
          </div>
        )}
        
        {/* Status badge */}
        <div className="absolute top-3 left-3">
          <div className={cn(
            "flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium border",
            config.className
          )}>
            <span className={cn("w-2 h-2 rounded-full status-pulse", config.dotClass)} />
            {config.label}
          </div>
        </div>
        
        {/* Camera ID */}
        <div className="absolute top-3 right-3">
          <span className="px-2 py-1 rounded bg-background/80 backdrop-blur text-xs font-mono text-muted-foreground">
            {id}
          </span>
        </div>
        
        {/* Expand button */}
        <button className="absolute bottom-3 right-3 p-2 rounded-lg bg-background/80 backdrop-blur text-foreground opacity-0 group-hover:opacity-100 transition-opacity">
          <Maximize2 className="w-4 h-4" />
        </button>
        
        {/* Alert overlay */}
        {status === "alert" && (
          <div className="absolute inset-0 bg-destructive/10 flex items-center justify-center">
            <div className="text-center">
              <AlertTriangle className="w-8 h-8 text-destructive mx-auto mb-2 animate-pulse" />
              <p className="text-xs font-medium text-destructive">Suspicious Activity</p>
            </div>
          </div>
        )}
      </div>
      
      <div className="p-4 space-y-1">
        <h3 className="font-semibold text-sm">{name}</h3>
        <p className="text-xs text-muted-foreground">{location}</p>
        {lastAlert && status === "alert" && (
          <p className="text-xs text-destructive font-medium mt-2">{lastAlert}</p>
        )}
      </div>
    </div>
  );
}
