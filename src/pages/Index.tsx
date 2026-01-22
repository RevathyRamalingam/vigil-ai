import { useState, useEffect, useRef } from "react";
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
  Scan,
  Monitor
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { api } from "@/services/api";
import { toast } from "sonner";
import Hls from "hls.js";

interface CameraData {
  id: string;
  name: string;
  location: string;
  status: string;
  stream_url?: string;
  is_live: boolean;
}

const Index = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [cameraStatus, setCameraStatus] = useState<"online" | "offline" | "alert">("online");
  const [lastScanTime, setLastScanTime] = useState<Date | null>(null);
  const [alerts, setAlerts] = useState<Array<{ id: string; message: string; time: string; severity: "high" | "medium" | "low" }>>([]);
  const [cameras, setCameras] = useState<CameraData[]>([]);
  const [selectedCamera, setSelectedCamera] = useState<CameraData | null>(null);

  const videoRef = useRef<HTMLVideoElement>(null);
  const hlsRef = useRef<Hls | null>(null);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    fetchCameras();

    return () => clearInterval(timer);
  }, []);

  const fetchCameras = async () => {
    try {
      const data = await api.getCameras();
      setCameras(data);
      if (data.length > 0 && !selectedCamera) {
        setSelectedCamera(data[0]);
      }
    } catch (error) {
      console.error("Failed to fetch cameras:", error);
    }
  };

  useEffect(() => {
    if (!videoRef.current || !selectedCamera) return;

    const video = videoRef.current;

    // Clean up previous HLS instance
    if (hlsRef.current) {
      hlsRef.current.destroy();
      hlsRef.current = null;
    }

    if (selectedCamera.is_live && selectedCamera.stream_url) {
      if (Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(selectedCamera.stream_url);
        hls.attachMedia(video);
        hlsRef.current = hls;
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        // Native HLS support (Safari)
        video.src = selectedCamera.stream_url;
      }
    } else {
      // Local video fallback or specific file
      video.src = "/static/videos/travel_video_normal.mp4";
    }

    return () => {
      if (hlsRef.current) {
        hlsRef.current.destroy();
      }
    };
  }, [selectedCamera]);

  const handleStartScan = async () => {
    setIsScanning(true);

    try {
      const data = await api.scan();

      if (data.alert) {
        setCameraStatus("alert");
        const newAlert = {
          id: Date.now().toString(),
          message: data.mcp_notified
            ? "CRITICAL ALERT: Potential weapon detected. Authorities notified via MCP."
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

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Sidebar - Camera List */}
        <div className="space-y-4">
          <div className="glass-panel rounded-xl p-4">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <Camera className="w-4 h-4 text-primary" />
              Cameras
            </h3>
            <div className="space-y-2">
              {cameras.map((cam) => (
                <button
                  key={cam.id}
                  onClick={() => setSelectedCamera(cam)}
                  className={cn(
                    "w-full flex items-center gap-3 p-3 rounded-lg transition-all text-left border",
                    selectedCamera?.id === cam.id
                      ? "bg-primary/10 border-primary text-primary"
                      : "bg-background/20 border-transparent hover:border-border"
                  )}
                >
                  <div className={cn(
                    "w-2 h-2 rounded-full",
                    cam.is_live ? "bg-success status-pulse" : "bg-muted-foreground"
                  )} />
                  <div className="flex-1 overflow-hidden">
                    <p className="text-sm font-medium truncate">{cam.name}</p>
                    <p className="text-[10px] text-muted-foreground truncate">{cam.location}</p>
                  </div>
                  {cam.is_live && <span className="text-[10px] font-bold text-success uppercase tracking-tighter">Live</span>}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Main Feed */}
        <div className="lg:col-span-2">
          <div className={cn(
            "glass-panel rounded-xl overflow-hidden transition-all duration-300",
            cameraStatus === "alert" && "border-destructive/50 glow-destructive"
          )}>
            <div className="relative aspect-video bg-black/90">
              <video
                ref={videoRef}
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
                  {selectedCamera?.name || "CAM-001"}
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
                  <h2 className="font-semibold">{selectedCamera?.name || "Select Camera"}</h2>
                  <p className="text-sm text-muted-foreground">{selectedCamera?.location || "N/A"}</p>
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
                <span className="text-success font-medium">{selectedCamera?.is_live ? "Live Stream" : "Static Feed"}</span>
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
