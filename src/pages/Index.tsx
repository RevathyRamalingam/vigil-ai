import { useState, useEffect } from "react";
import { Camera, AlertTriangle, Shield, Activity, Eye } from "lucide-react";
import { Header } from "@/components/dashboard/Header";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { CameraFeed } from "@/components/dashboard/CameraFeed";
import { AlertItem } from "@/components/dashboard/AlertItem";
import { ActivityTimeline } from "@/components/dashboard/ActivityTimeline";
import { ScanStatus } from "@/components/dashboard/ScanStatus";

// Mock data
const mockCameras = [
  { id: "CAM-001", name: "Main Street East", location: "123 Main St, Junction A", status: "online" as const },
  { id: "CAM-002", name: "Downtown Plaza", location: "456 Commerce Ave", status: "alert" as const, lastAlert: "Unidentified person loitering" },
  { id: "CAM-003", name: "Industrial Zone Gate", location: "789 Factory Rd, Entry B", status: "online" as const },
  { id: "CAM-004", name: "Residential Block 4", location: "321 Oak Lane", status: "offline" as const },
  { id: "CAM-005", name: "Park Avenue North", location: "654 Park Ave, Sector 2", status: "online" as const },
  { id: "CAM-006", name: "Mall Parking Lot", location: "987 Shopping Center", status: "alert" as const, lastAlert: "Suspicious vehicle detected" },
];

const mockAlerts = [
  { id: "ALT-001", type: "suspicious_person" as const, severity: "high" as const, title: "Unidentified person loitering", location: "Downtown Plaza", timestamp: "2 min ago", cameraId: "CAM-002" },
  { id: "ALT-002", type: "vehicle" as const, severity: "medium" as const, title: "Suspicious vehicle detected", location: "Mall Parking Lot", timestamp: "5 min ago", cameraId: "CAM-006" },
  { id: "ALT-003", type: "intrusion" as const, severity: "low" as const, title: "Motion detected after hours", location: "Industrial Zone Gate", timestamp: "12 min ago", cameraId: "CAM-003" },
  { id: "ALT-004", type: "general" as const, severity: "medium" as const, title: "Unusual crowd gathering", location: "Main Street East", timestamp: "18 min ago", cameraId: "CAM-001" },
];

const mockActivities = [
  { id: "ACT-001", type: "alert" as const, message: "Alert triggered at CAM-002", timestamp: "14:32:15" },
  { id: "ACT-002", type: "scan" as const, message: "AI scan completed - 6 cameras analyzed", timestamp: "14:30:00" },
  { id: "ACT-003", type: "clear" as const, message: "CAM-005 returned to normal status", timestamp: "14:28:45" },
  { id: "ACT-004", type: "camera" as const, message: "CAM-004 went offline", timestamp: "14:25:12" },
  { id: "ACT-005", type: "scan" as const, message: "Starting scheduled patrol scan", timestamp: "14:25:00" },
  { id: "ACT-006", type: "alert" as const, message: "Suspicious activity at CAM-006", timestamp: "14:22:33" },
  { id: "ACT-007", type: "clear" as const, message: "All zones cleared - routine check", timestamp: "14:20:00" },
];

const Index = () => {
  const [isScanning, setIsScanning] = useState(true);
  const [scanProgress, setScanProgress] = useState(67);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    // Simulate scan progress
    const scanTimer = setInterval(() => {
      setScanProgress((prev) => {
        if (prev >= 100) {
          setIsScanning(false);
          return 0;
        }
        return prev + 5;
      });
    }, 1000);

    return () => {
      clearInterval(timer);
      clearInterval(scanTimer);
    };
  }, []);

  const onlineCameras = mockCameras.filter(c => c.status !== "offline").length;
  const activeAlerts = mockCameras.filter(c => c.status === "alert").length;

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="p-6 space-y-6">
        {/* Top Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatsCard
            title="Cameras Online"
            value={`${onlineCameras}/${mockCameras.length}`}
            icon={Camera}
            variant="success"
          />
          <StatsCard
            title="Active Alerts"
            value={activeAlerts}
            icon={AlertTriangle}
            variant="destructive"
            trend={{ value: 15, isPositive: false }}
          />
          <StatsCard
            title="Incidents Today"
            value={12}
            icon={Shield}
            variant="warning"
          />
          <StatsCard
            title="AI Scans Today"
            value={248}
            icon={Eye}
            trend={{ value: 8, isPositive: true }}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content Area */}
          <div className="lg:col-span-2 space-y-6">
            {/* Camera Grid */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold flex items-center gap-2">
                  <Camera className="w-5 h-5 text-primary" />
                  Live Camera Feeds
                </h2>
                <div className="flex items-center gap-2 text-xs text-muted-foreground font-mono">
                  <Activity className="w-4 h-4" />
                  {currentTime.toLocaleTimeString()}
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                {mockCameras.map((camera) => (
                  <CameraFeed key={camera.id} {...camera} />
                ))}
              </div>
            </div>

            {/* Recent Alerts */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-destructive" />
                  Recent Alerts
                </h2>
                <button className="text-xs text-primary hover:underline">View all</button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {mockAlerts.map((alert) => (
                  <AlertItem key={alert.id} {...alert} />
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <ScanStatus
              isScanning={isScanning}
              lastScan="14:30:00"
              nextScan="14:35:00"
              progress={scanProgress}
              camerasScanned={4}
              totalCameras={6}
            />
            <ActivityTimeline activities={mockActivities} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
