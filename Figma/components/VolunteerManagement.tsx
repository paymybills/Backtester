import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Search, UserPlus, Mail, Phone, MapPin } from "lucide-react";
import { useState } from "react";

export function VolunteerManagement() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRole, setSelectedRole] = useState("all");

  // Mock volunteer data
  const volunteers = [
    {
      id: "VOL-001",
      name: "Alice Thompson",
      email: "alice.thompson@email.com",
      phone: "(555) 123-4567",
      role: "Registration Desk",
      status: "Present",
      checkInTime: "5:30 AM",
      location: "Main Entrance"
    },
    {
      id: "VOL-002", 
      name: "Bob Martinez",
      email: "bob.martinez@email.com",
      phone: "(555) 234-5678",
      role: "Water Station",
      status: "Present",
      checkInTime: "5:45 AM",
      location: "Mile 5"
    },
    {
      id: "VOL-003",
      name: "Carol Davis",
      email: "carol.davis@email.com", 
      phone: "(555) 345-6789",
      role: "Course Marshal",
      status: "Present",
      checkInTime: "6:00 AM",
      location: "Mile 10"
    },
    {
      id: "VOL-004",
      name: "David Wilson",
      email: "david.wilson@email.com",
      phone: "(555) 456-7890",
      role: "Medical Team",
      status: "Present",
      checkInTime: "5:15 AM",
      location: "Medical Tent"
    },
    {
      id: "VOL-005",
      name: "Emma Brown",
      email: "emma.brown@email.com",
      phone: "(555) 567-8901",
      role: "Finish Line",
      status: "Present",
      checkInTime: "6:15 AM",
      location: "Finish Area"
    },
    {
      id: "VOL-006",
      name: "Frank Johnson",
      email: "frank.johnson@email.com",
      phone: "(555) 678-9012",
      role: "Water Station",
      status: "Missing",
      checkInTime: "-",
      location: "Mile 15"
    },
    {
      id: "VOL-007",
      name: "Grace Lee",
      email: "grace.lee@email.com",
      phone: "(555) 789-0123",
      role: "Photography",
      status: "Present",
      checkInTime: "6:30 AM",
      location: "Various"
    },
    {
      id: "VOL-008",
      name: "Henry Clark",
      email: "henry.clark@email.com",
      phone: "(555) 890-1234",
      role: "Course Marshal",
      status: "Present",
      checkInTime: "5:50 AM",
      location: "Mile 20"
    }
  ];

  const roles = [
    "Registration Desk",
    "Water Station", 
    "Course Marshal",
    "Medical Team",
    "Finish Line",
    "Photography",
    "Setup Crew",
    "Cleanup Crew"
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Present":
        return <Badge className="bg-green-100 text-green-800">Present</Badge>;
      case "Missing":
        return <Badge variant="destructive">Missing</Badge>;
      case "Late":
        return <Badge className="bg-yellow-100 text-yellow-800">Late</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  const filteredVolunteers = volunteers.filter(volunteer => {
    const matchesSearch = volunteer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         volunteer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         volunteer.role.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = selectedRole === "all" || volunteer.role === selectedRole;
    return matchesSearch && matchesRole;
  });

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1>Volunteer Management</h1>
        <p className="text-muted-foreground">Manage volunteer assignments and track attendance</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Volunteers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">89</div>
            <p className="text-xs text-green-600">8 assigned today</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Present</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">83</div>
            <p className="text-xs text-muted-foreground">93% attendance</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Missing</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">6</div>
            <p className="text-xs text-muted-foreground">Need replacements</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Roles Filled</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">94%</div>
            <p className="text-xs text-green-600">All critical covered</p>
          </CardContent>
        </Card>
      </div>

      {/* Controls */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Volunteer Directory</CardTitle>
            <div className="flex gap-2">
              <Button>
                <UserPlus className="mr-2 h-4 w-4" />
                Add Volunteer
              </Button>
              <Button variant="outline">
                Assign Roles
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4 mb-6">
            {/* Search Bar */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search volunteers by name, email, or role..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            {/* Role Filter */}
            <Select value={selectedRole} onValueChange={setSelectedRole}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filter by role" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Roles</SelectItem>
                {roles.map((role) => (
                  <SelectItem key={role} value={role}>{role}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Volunteers Table */}
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Volunteer</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Contact</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Check-in</TableHead>
                <TableHead>Location</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredVolunteers.map((volunteer) => (
                <TableRow key={volunteer.id}>
                  <TableCell>
                    <div>
                      <div className="font-medium">{volunteer.name}</div>
                      <div className="text-xs text-muted-foreground font-mono">{volunteer.id}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">{volunteer.role}</Badge>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="flex items-center gap-1 text-xs">
                        <Mail className="h-3 w-3" />
                        <span className="truncate max-w-32">{volunteer.email}</span>
                      </div>
                      <div className="flex items-center gap-1 text-xs">
                        <Phone className="h-3 w-3" />
                        <span>{volunteer.phone}</span>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>{getStatusBadge(volunteer.status)}</TableCell>
                  <TableCell className="text-sm">
                    {volunteer.checkInTime}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1 text-sm">
                      <MapPin className="h-3 w-3" />
                      {volunteer.location}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Button size="sm" variant="outline">
                        Edit
                      </Button>
                      <Button size="sm" variant="outline">
                        Message
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredVolunteers.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <Search className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <div>No volunteers found matching your search criteria</div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button variant="outline" className="w-full justify-start">
              Send Check-in Reminder
            </Button>
            <Button variant="outline" className="w-full justify-start">
              Export Volunteer List
            </Button>
            <Button variant="outline" className="w-full justify-start">
              Generate Name Tags
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Communication</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button variant="outline" className="w-full justify-start">
              <Mail className="mr-2 h-4 w-4" />
              Email All Volunteers
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <Phone className="mr-2 h-4 w-4" />
              Call Missing Volunteers
            </Button>
            <Button variant="outline" className="w-full justify-start">
              Send Role Updates
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Reports</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button variant="outline" className="w-full justify-start">
              Attendance Report
            </Button>
            <Button variant="outline" className="w-full justify-start">
              Role Assignment Summary
            </Button>
            <Button variant="outline" className="w-full justify-start">
              Contact Directory
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}