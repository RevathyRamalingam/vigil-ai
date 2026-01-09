import { cn } from "@/lib/utils";
import { Scan, Clock, Activity } from "lucide-react";
import { Progress } from "@/components/ui/progress";

interface ScanStatusProps {
  isScanning: boolean;
  lastScan: string;
  nextScan: string;
  progress: number;
  camerasScanned: number;
  totalCameras: number;
}

export function ScanStatus({ 
  isScanning, 
  lastScan, 
  nextScan, 
  progress, 
  camerasScanned, 
  totalCameras 
}: ScanStatusProps) {
  return (
    <div className={cn(
      "glass-panel rounded-lg p-4 transition-all duration-300",
      isScanning && "border-primary/50 glow-primary"
    )}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className={cn(
            "p-2 rounded-lg",
            isScanning ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground"
          )}>
            <Scan className={cn("w-5 h-5", isScanning && "animate-spin")} />
          </div>
          <div>
            <h3 className="font-semibold text-sm">Patrol Scan</h3>
            <p className="text-xs text-muted-foreground">
              {isScanning ? "Scanning in progress..." : "Awaiting next scan"}
            </p>
          </div>
        </div>
        
        <div className={cn(
          "px-3 py-1 rounded-full text-xs font-medium",
          isScanning 
            ? "bg-primary/20 text-primary border border-primary/30" 
            : "bg-muted text-muted-foreground"
        )}>
          {isScanning ? "Active" : "Idle"}
        </div>
      </div>
      
      {isScanning && (
        <div className="space-y-3 mb-4">
          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">Progress</span>
            <span className="font-mono text-primary">{camerasScanned}/{totalCameras} cameras</span>
          </div>
          <Progress value={progress} className="h-1.5" />
        </div>
      )}
      
      <div className="grid grid-cols-2 gap-4 pt-3 border-t border-border/50">
        <div className="flex items-center gap-2 text-xs">
          <Clock className="w-3.5 h-3.5 text-muted-foreground" />
          <div>
            <p className="text-muted-foreground">Last Scan</p>
            <p className="font-mono">{lastScan}</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <Activity className="w-3.5 h-3.5 text-primary" />
          <div>
            <p className="text-muted-foreground">Next Scan</p>
            <p className="font-mono text-primary">{nextScan}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
