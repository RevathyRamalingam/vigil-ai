import { useState, useEffect } from "react";
import { 
  Camera, 
  AlertTriangle, 
  Shield, 
  Play, 
  Pause, 
  Maximize2,
  Settings,
  Bell,
  CheckCircle,
  Clock,
  Scan
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const Index = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [cameraStatus, setCameraStatus] = useState<"online" | "offline" | "alert">("online");
  const [alerts, setAlerts] = useState<Array<{ id: string; message: string; time: string; severity: "high" | "medium" | "low" }>>([
    { id: "1", message: "Motion detected in restricted area", time: "2 min ago", severity: "high" },
    { id: "2", message: "Unusual activity pattern", time: "15 min ago", severity: "medium" },
  ]);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleStartScan = () => {
    setIsScanning(true);
    // Simulate scan completion
    setTimeout(() => {
      setIsScanning(false);
    }, 5000);
  };

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10 glow-primary">
            <Shield className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h1 className="text-xl font-bold">PatrolVision</h1>
            <p className="text-xs text-muted-foreground">Street Camera Monitor</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <span className="text-sm font-mono text-muted-foreground">
            {currentTime.toLocaleTimeString()}
          </span>
          <Button variant="ghost" size="icon" className="relative">
            <Bell className="w-5 h-5" />
            {alerts.length > 0 && (
              <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-destructive status-pulse" />
            )}
          </Button>
          <Button variant="ghost" size="icon">
            <Settings className="w-5 h-5" />
          </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Camera Feed */}
        <div className="lg:col-span-2">
          <div className={cn(
            "glass-panel rounded-xl overflow-hidden transition-all duration-300",
            cameraStatus === "alert" && "border-destructive/50 glow-destructive"
          )}>
            {/* Camera View */}
            <div className="relative aspect-video bg-muted/30">
              <div className="absolute inset-0 flex items-center justify-center">
                <Camera className="w-20 h-20 text-muted-foreground/30" />
              </div>
              
              {/* Scan line effect */}
              {isScanning && (
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                  <div className="absolute w-full h-1 bg-gradient-to-r from-transparent via-primary/50 to-transparent scan-line" />
                </div>
              )}
              
              {/* Status Badge */}
              <div className="absolute top-4 left-4">
                <div className={cn(
                  "flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium border backdrop-blur",
                  cameraStatus === "online" && "bg-success/20 text-success border-success/30",
                  cameraStatus === "alert" && "bg-destructive/20 text-destructive border-destructive/30",
                  cameraStatus === "offline" && "bg-muted text-muted-foreground border-border"
                )}>
                  <span className={cn(
                    "w-2 h-2 rounded-full status-pulse",
                    cameraStatus === "online" && "bg-success",
                    cameraStatus === "alert" && "bg-destructive",
                    cameraStatus === "offline" && "bg-muted-foreground"
                  )} />
                  {cameraStatus === "online" && "Live"}
                  {cameraStatus === "alert" && "Alert"}
                  {cameraStatus === "offline" && "Offline"}
                </div>
              </div>
              
              {/* Camera ID */}
              <div className="absolute top-4 right-4">
                <span className="px-3 py-1.5 rounded-lg bg-background/80 backdrop-blur text-sm font-mono">
                  CAM-001
                </span>
              </div>
              
              {/* Time Overlay */}
              <div className="absolute bottom-4 left-4">
                <span className="px-3 py-1.5 rounded-lg bg-background/80 backdrop-blur text-sm font-mono text-primary">
                  {currentTime.toLocaleString()}
                </span>
              </div>
              
              {/* Fullscreen Button */}
              <button className="absolute bottom-4 right-4 p-2 rounded-lg bg-background/80 backdrop-blur hover:bg-background/90 transition-colors">
                <Maximize2 className="w-5 h-5" />
              </button>
            </div>
            
            {/* Camera Info & Controls */}
            <div className="p-4 border-t border-border/50">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="font-semibold">Main Street Camera</h2>
                  <p className="text-sm text-muted-foreground">123 Main St, Downtown</p>
                </div>
                
                <div className="flex items-center gap-2">
                  <Button
                    onClick={handleStartScan}
                    disabled={isScanning}
                    className={cn(
                      "gap-2",
                      isScanning && "bg-primary/20"
                    )}
                  >
                    <Scan className={cn("w-4 h-4", isScanning && "animate-spin")} />
                    {isScanning ? "Scanning..." : "Scan Now"}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Status Card */}
          <div className="glass-panel rounded-xl p-4">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-success" />
              System Status
            </h3>
            
            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Camera</span>
                <span className="text-success font-medium">Online</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Last Scan</span>
                <span className="font-mono">14:30:00</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Next Scan</span>
                <span className="font-mono text-primary">14:35:00</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Scans Today</span>
                <span className="font-mono">48</span>
              </div>
            </div>
          </div>

          {/* Alerts */}
          <div className="glass-panel rounded-xl p-4">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-destructive" />
              Recent Alerts
              <span className="ml-auto px-2 py-0.5 rounded-full bg-destructive/20 text-destructive text-xs">
                {alerts.length}
              </span>
            </h3>
            
            <div className="space-y-3">
              {alerts.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">
                  No alerts
                </p>
              ) : (
                alerts.map((alert) => (
                  <div 
                    key={alert.id}
                    className={cn(
                      "p-3 rounded-lg border-l-4",
                      alert.severity === "high" && "bg-destructive/5 border-l-destructive",
                      alert.severity === "medium" && "bg-warning/5 border-l-warning",
                      alert.severity === "low" && "bg-primary/5 border-l-primary"
                    )}
                  >
                    <p className="text-sm font-medium">{alert.message}</p>
                    <p className="text-xs text-muted-foreground flex items-center gap-1 mt-1">
                      <Clock className="w-3 h-3" />
                      {alert.time}
                    </p>
                  </div>
                ))
              )}
            </div>
            
            {alerts.length > 0 && (
              <Button variant="ghost" className="w-full mt-3 text-sm">
                View All Alerts
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
