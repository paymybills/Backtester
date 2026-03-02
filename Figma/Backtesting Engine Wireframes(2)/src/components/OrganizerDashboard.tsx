import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts";

export function OrganizerDashboard() {
  // Mock registration data
  const registrationStats = [
    { label: "Total Registrations", value: "2,847", change: "+127 today" },
    { label: "Check-ins Completed", value: "1,923", change: "67% complete" },
    { label: "Active Volunteers", value: "89", change: "94% assigned" },
    { label: "Runners on Course", value: "1,576", change: "Live tracking" },
  ];

  // Mock recent registrations
  const recentRegistrations = [
    { id: "REG-2847", name: "Sarah Johnson", category: "Full Marathon", time: "2 mins ago", status: "Confirmed" },
    { id: "REG-2846", name: "Mike Chen", category: "Half Marathon", time: "5 mins ago", status: "Confirmed" },
    { id: "REG-2845", name: "Emma Davis", category: "10K", time: "8 mins ago", status: "Pending" },
    { id: "REG-2844", name: "David Wilson", category: "Full Marathon", time: "12 mins ago", status: "Confirmed" },
    { id: "REG-2843", name: "Lisa Brown", category: "Half Marathon", time: "15 mins ago", status: "Confirmed" },
  ];

  // Mock volunteer data
  const volunteerSummary = [
    { role: "Registration Desk", assigned: 12, present: 11, status: "active" },
    { role: "Water Stations", assigned: 24, present: 22, status: "active" },
    { role: "Course Marshals", assigned: 18, present: 17, status: "active" },
    { role: "Medical Team", assigned: 8, present: 8, status: "active" },
    { role: "Finish Line", assigned: 15, present: 14, status: "active" },
    { role: "Photography", assigned: 6, present: 5, status: "partial" },
  ];

  // Mock analytics data
  const registrationTrend = [
    { month: "Jan", registrations: 145 },
    { month: "Feb", registrations: 298 },
    { month: "Mar", registrations: 523 },
    { month: "Apr", registrations: 847 },
    { month: "May", registrations: 1245 },
    { month: "Jun", registrations: 1678 },
    { month: "Jul", registrations: 2134 },
    { month: "Aug", registrations: 2555 },
    { month: "Sep", registrations: 2847 },
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Confirmed":
        return <Badge variant="default" className="bg-green-100 text-green-800">Confirmed</Badge>;
      case "Pending":
        return <Badge variant="secondary">Pending</Badge>;
      case "Cancelled":
        return <Badge variant="destructive">Cancelled</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  const getVolunteerStatus = (status: string) => {
    switch (status) {
      case "active":
        return <Badge variant="default" className="bg-green-100 text-green-800">Active</Badge>;
      case "partial":
        return <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">Partial</Badge>;
      case "missing":
        return <Badge variant="destructive">Missing</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1>Organizer Dashboard</h1>
        <p className="text-muted-foreground">Marathon event overview and real-time statistics</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {registrationStats.map((stat, index) => (
          <Card key={index}>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.label}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-green-600">{stat.change}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Online Registrations Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Online Registrations Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={registrationTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="registrations" 
                  stroke="#2563eb" 
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Volunteer Status Overview */}
        <Card>
          <CardHeader>
            <CardTitle>Volunteer Status Overview</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {volunteerSummary.map((volunteer, index) => (
              <div key={index} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">{volunteer.role}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">
                      {volunteer.present}/{volunteer.assigned}
                    </span>
                    {getVolunteerStatus(volunteer.status)}
                  </div>
                </div>
                <Progress 
                  value={(volunteer.present / volunteer.assigned) * 100} 
                  className="h-2"
                />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Registrations */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Online Registrations</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Participant</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentRegistrations.map((registration) => (
                  <TableRow key={registration.id}>
                    <TableCell className="font-mono text-sm">{registration.id}</TableCell>
                    <TableCell>
                      <div>
                        <div className="font-medium">{registration.name}</div>
                        <div className="text-xs text-muted-foreground">{registration.time}</div>
                      </div>
                    </TableCell>
                    <TableCell>{registration.category}</TableCell>
                    <TableCell>{getStatusBadge(registration.status)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Live Runner Tracking Summary */}
        <Card>
          <CardHeader>
            <CardTitle>Live Runner Tracking</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-blue-600">1,576</div>
                <div className="text-sm text-muted-foreground">Active Trackers</div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-green-600">847</div>
                <div className="text-sm text-muted-foreground">Finished</div>
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm">Course Completion</span>
                <span className="text-sm font-medium">35%</span>
              </div>
              <Progress value={35} className="h-2" />
              
              <div className="flex justify-between">
                <span className="text-sm">Average Pace</span>
                <span className="text-sm font-medium">8:45 min/mile</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-sm">Est. Finish Time Range</span>
                <span className="text-sm font-medium">3:45 - 6:30</span>
              </div>
            </div>

            <div className="pt-4 border-t">
              <div className="text-sm font-medium mb-2">Recent Checkpoint Activity</div>
              <div className="space-y-1 text-xs text-muted-foreground">
                <div>• Mile 15: 1,234 runners passed (2 mins ago)</div>
                <div>• Mile 10: 1,456 runners passed (8 mins ago)</div>
                <div>• Mile 5: 1,598 runners passed (15 mins ago)</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}