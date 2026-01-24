import { useState, useEffect, useRef } from "react";
import {
  AlertTriangle,
  Shield,
  Maximize2,
  Settings,
  Bell,
  CheckCircle,
  Clock,
  Scan,
  PlayCircle,
  AlertOctagon
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { api } from "@/services/api";
import { toast } from "sonner";

// Video configuration
const VIDEO_PATHS = {
  normal: {
    path: "/static/videos/travel_video_normal.mp4",
    filename: "travel_video_normal.mp4",
    label: "Normal Activity"
  },
  suspicious: {
    path: "/static/videos/Burglary001_x264_14.mp4",
    filename: "Burglary001_x264_14.mp4",
    label: "Suspicious Activity"
  }
};

const Index = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [cameraStatus, setCameraStatus] = useState<"online" | "offline" | "alert">("online");
  const [lastScanTime, setLastScanTime] = useState<Date | null>(null);
  const [alerts, setAlerts] = useState<Array<{ id: string; message: string; time: string; severity: "high" | "medium" | "low" }>>([]);

  // Demo State
  const [activeVideo, setActiveVideo] = useState<"normal" | "suspicious">("normal");

  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleStartScan = async () => {
    setIsScanning(true);

    try {
      // Pass the specific filename for the currently active video
      const filename = VIDEO_PATHS[activeVideo].filename;
      const data = await api.scan(filename);

      if (data.alert) {
        setCameraStatus("alert");
        const newAlert = {
          id: Date.now().toString(),
          message: data.mcp_notified
            ? "CRITICAL ALERT: Suspicious activity detected. Authorities notified via MCP."
            : "Suspicious activity detected during scan",
          time: "Just now",
          severity: data.mcp_notified ? "high" as const : "medium" as const
        };
        setAlerts(prev => [newAlert, ...prev]);

        if (data.mcp_notified) {
          toast.error("POLICE NOTIFIED", {
            description: "Critical alert dispatched to Police Control Room via MCP interaction.",
            duration: 10000,
          });
        }
      } else {
        setCameraStatus("online");
      }

      const scanTime = new Date();
      setLastScanTime(scanTime);
    } catch (error) {
      toast.error("Scan failed", { description: "Backend not reachable or internal error." });
    } finally {
      setIsScanning(false);
    }
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
            <h1 className="text-xl font-bold">VigilAI</h1>
            <p className="text-xs text-muted-foreground">Vigilance Monitor</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Demo Controls */}
          <div className="flex items-center gap-2 mr-4 bg-muted/30 p-1 rounded-lg border border-border/50">
            <Button
              variant={activeVideo === "normal" ? "secondary" : "ghost"}
              size="sm"
              onClick={() => setActiveVideo("normal")}
              className={cn("gap-2 text-xs", activeVideo === "normal" && "bg-background shadow-sm")}
            >
              <PlayCircle className="w-3.5 h-3.5" />
              Normal
            </Button>
            <Button
              variant={activeVideo === "suspicious" ? "destructive" : "ghost"}
              size="sm"
              onClick={() => setActiveVideo("suspicious")}
              className={cn("gap-2 text-xs", activeVideo === "suspicious" && "shadow-sm")}
            >
              <AlertOctagon className="w-3.5 h-3.5" />
              Suspicious
            </Button>
          </div>

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

        {/* Main Feed */}
        <div className="lg:col-span-2">
          <div className={cn(
            "glass-panel rounded-xl overflow-hidden transition-all duration-300",
            cameraStatus === "alert" && "border-destructive/50 glow-destructive"
          )}>
            <div className="relative aspect-video bg-black/90">
              <video
                key={activeVideo} // key ensures video reloads when source changes
                ref={videoRef}
                src={VIDEO_PATHS[activeVideo].path}
                autoPlay
                muted
                loop
                playsInline
                className="absolute inset-0 w-full h-full object-cover opacity-80"
              />

              <div className="absolute inset-0 pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20" />

              {isScanning && (
                <div className="absolute inset-0 overflow-hidden pointer-events-none z-10">
                  <div className="absolute w-full h-1 bg-gradient-to-r from-transparent via-primary/50 to-transparent scan-line" />
                </div>
              )}

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

              <div className="absolute top-4 right-4 flex flex-col items-end gap-2">
                <span className="px-3 py-1.5 rounded-lg bg-background/80 backdrop-blur text-sm font-mono z-10">
                  CAM-DEMO-01
                </span>
                <div className="flex items-center gap-2 px-2 py-1 rounded bg-destructive/20 border border-destructive/30 backdrop-blur z-10">
                  <span className="w-2 h-2 rounded-full bg-destructive animate-pulse" />
                  <span className="text-[10px] font-bold text-destructive tracking-widest uppercase">REC</span>
                </div>
              </div>

              <div className="absolute bottom-4 left-4">
                <span className="px-3 py-1.5 rounded-lg bg-background/80 backdrop-blur text-sm font-mono text-primary">
                  {currentTime.toLocaleString()}
                </span>
              </div>

              <button className="absolute bottom-4 right-4 p-2 rounded-lg bg-background/80 backdrop-blur hover:bg-background/90 transition-colors">
                <Maximize2 className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 border-t border-border/50">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="font-semibold">Demo Feed: {VIDEO_PATHS[activeVideo].label}</h2>
                  <p className="text-sm text-muted-foreground">Scenario Simulation Mode</p>
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

        {/* Right Sidebar */}
        <div className="space-y-6">
          <div className="glass-panel rounded-xl p-4">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-success" />
              System Status
            </h3>

            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Source</span>
                <span className="text-success font-medium">Demo Video</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Last Scan</span>
                <span className="font-mono">{lastScanTime ? lastScanTime.toLocaleTimeString() : "N/A"}</span>
              </div>
            </div>
          </div>

          <div className="glass-panel rounded-xl p-4">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-destructive" />
              Recent Alerts
              <span className="ml-auto px-2 py-0.5 rounded-full bg-destructive/20 text-destructive text-xs">
                {alerts.length}
              </span>
            </h3>

            <div className="space-y-3 max-h-[400px] overflow-y-auto pr-1">
              {alerts.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">No alerts</p>
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
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
