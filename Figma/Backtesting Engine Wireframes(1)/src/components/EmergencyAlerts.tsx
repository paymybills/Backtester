import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { AlertTriangle, MapPin, Clock, Phone, Radio, Ambulance } from "lucide-react";
import { useState } from "react";

export function EmergencyAlerts() {
  const [alertType, setAlertType] = useState("");
  const [alertDescription, setAlertDescription] = useState("");

  // Mock active alerts data
  const activeAlerts = [
    {
      id: "EMR-001",
      type: "Medical",
      priority: "High",
      status: "Active",
      location: "Mile 12.5",
      coordinates: "40.7589, -73.9851",
      description: "Runner collapsed, conscious but dizzy",
      reportedBy: "Volunteer Mary Smith",
      timeReported: "8:45 AM",
      responders: ["Medical Team 2", "Course Marshal C"],
      estimatedResponse: "3 minutes"
    },
    {
      id: "EMR-002", 
      type: "Course Issue",
      priority: "Medium",
      status: "Resolved",
      location: "Mile 8.2",
      coordinates: "40.7505, -73.9934",
      description: "Fallen tree blocking course",
      reportedBy: "Course Marshal B",
      timeReported: "8:30 AM",
      responders: ["Maintenance Crew", "Course Marshal B"],
      estimatedResponse: "Resolved"
    },
    {
      id: "EMR-003",
      type: "Weather",
      priority: "Low",
      status: "Monitoring",
      location: "Mile 15-20",
      coordinates: "40.7829, -73.9654",
      description: "Light rain reported, monitoring conditions",
      reportedBy: "Weather Station",
      timeReported: "8:20 AM",
      responders: ["Event Director"],
      estimatedResponse: "Ongoing"
    }
  ];

  const emergencyContacts = [
    { role: "Event Director", name: "John Smith", phone: "(555) 911-0001" },
    { role: "Medical Director", name: "Dr. Sarah Wilson", phone: "(555) 911-0002" },
    { role: "Security Chief", name: "Mike Johnson", phone: "(555) 911-0003" },
    { role: "Course Director", name: "Lisa Davis", phone: "(555) 911-0004" }
  ];

  const alertTypes = [
    "Medical Emergency",
    "Course Issue", 
    "Weather Alert",
    "Security Incident",
    "Equipment Failure",
    "Missing Person",
    "Other"
  ];

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case "High":
        return <Badge variant="destructive">High Priority</Badge>;
      case "Medium":
        return <Badge className="bg-yellow-100 text-yellow-800">Medium Priority</Badge>;
      case "Low":
        return <Badge variant="secondary">Low Priority</Badge>;
      default:
        return <Badge variant="secondary">{priority}</Badge>;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Active":
        return <Badge className="bg-red-100 text-red-800 animate-pulse">Active</Badge>;
      case "Resolved":
        return <Badge className="bg-green-100 text-green-800">Resolved</Badge>;
      case "Monitoring":
        return <Badge className="bg-blue-100 text-blue-800">Monitoring</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  const handleRaiseAlert = () => {
    if (alertType && alertDescription) {
      // In a real app, this would send the alert to the system
      console.log("Alert raised:", { type: alertType, description: alertDescription });
      setAlertType("");
      setAlertDescription("");
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center gap-3">
        <AlertTriangle className="h-6 w-6 text-red-600" />
        <div>
          <h1>Emergency Alert System</h1>
          <p className="text-muted-foreground">Medical team and organizer emergency response center</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Raise Emergency Alert */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-600">
              <AlertTriangle className="h-5 w-5" />
              Raise Emergency Alert
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Alert Type</label>
              <Select value={alertType} onValueChange={setAlertType}>
                <SelectTrigger>
                  <SelectValue placeholder="Select emergency type" />
                </SelectTrigger>
                <SelectContent>
                  {alertTypes.map((type) => (
                    <SelectItem key={type} value={type}>{type}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Description & Location</label>
              <Textarea
                placeholder="Describe the emergency and provide specific location details (mile marker, landmark, GPS coordinates if available)..."
                value={alertDescription}
                onChange={(e) => setAlertDescription(e.target.value)}
                className="h-24"
              />
            </div>

            <div className="flex gap-3">
              <Button 
                onClick={handleRaiseAlert}
                className="flex-1 bg-red-600 hover:bg-red-700 text-white"
                disabled={!alertType || !alertDescription}
              >
                <AlertTriangle className="mr-2 h-4 w-4" />
                RAISE EMERGENCY ALERT
              </Button>
              <Button variant="outline">
                <Phone className="mr-2 h-4 w-4" />
                Call 911
              </Button>
            </div>

            <div className="text-xs text-muted-foreground bg-gray-50 p-3 rounded">
              <strong>Emergency Protocol:</strong> For life-threatening emergencies, call 911 immediately. 
              Use this system for course incidents, non-critical medical issues, and coordination alerts.
            </div>
          </CardContent>
        </Card>

        {/* Emergency Contacts */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Phone className="h-4 w-4" />
              Emergency Contacts
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {emergencyContacts.map((contact, index) => (
              <div key={index} className="flex justify-between items-center p-3 border rounded-lg">
                <div>
                  <div className="font-medium text-sm">{contact.role}</div>
                  <div className="text-xs text-muted-foreground">{contact.name}</div>
                </div>
                <Button size="sm" variant="outline">
                  <Phone className="h-3 w-3 mr-1" />
                  Call
                </Button>
              </div>
            ))}
            
            <div className="pt-3 border-t">
              <Button variant="outline" className="w-full">
                <Radio className="mr-2 h-4 w-4" />
                Radio All Teams
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Active Alerts */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              Active Emergency Alerts
            </CardTitle>
            <div className="text-sm text-muted-foreground">
              {activeAlerts.filter(alert => alert.status === "Active").length} active alerts
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Alert ID</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Priority</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Location</TableHead>
                <TableHead>Time</TableHead>
                <TableHead>Responders</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {activeAlerts.map((alert) => (
                <TableRow key={alert.id} className={alert.status === "Active" ? "bg-red-50" : ""}>
                  <TableCell className="font-mono text-sm">{alert.id}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{alert.type}</Badge>
                  </TableCell>
                  <TableCell>{getPriorityBadge(alert.priority)}</TableCell>
                  <TableCell>{getStatusBadge(alert.status)}</TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="flex items-center gap-1 text-sm">
                        <MapPin className="h-3 w-3" />
                        {alert.location}
                      </div>
                      <div className="text-xs text-muted-foreground font-mono">
                        {alert.coordinates}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1 text-sm">
                      <Clock className="h-3 w-3" />
                      {alert.timeReported}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      {alert.responders.map((responder, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {responder}
                        </Badge>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Button size="sm" variant="outline">
                        View
                      </Button>
                      {alert.status === "Active" && (
                        <Button size="sm" variant="outline">
                          Resolve
                        </Button>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* System Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Response Teams</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">8</div>
            <p className="text-xs text-green-600">All teams active</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Avg Response Time</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4:32</div>
            <p className="text-xs text-muted-foreground">minutes</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Alerts Today</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-green-600">3 resolved</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}