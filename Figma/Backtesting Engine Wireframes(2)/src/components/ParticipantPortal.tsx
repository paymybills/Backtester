import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { MapPin, Clock, Trophy, Download } from "lucide-react";

export function ParticipantPortal() {
  // Mock participant data
  const participantInfo = {
    name: "Sarah Johnson",
    email: "sarah.johnson@email.com",
    registrationId: "REG-2847",
    bibNumber: "A-1247",
    category: "Full Marathon",
    startTime: "7:00 AM",
    wave: "Wave A",
    status: "Confirmed"
  };

  const raceResults = {
    finishTime: "4:23:15",
    overallPlace: "347",
    categoryPlace: "89",
    pace: "10:03",
    splits: [
      { checkpoint: "5K", time: "23:45", pace: "7:38" },
      { checkpoint: "10K", time: "47:32", pace: "7:40" },
      { checkpoint: "Half", time: "1:44:23", pace: "7:58" },
      { checkpoint: "30K", time: "2:35:47", pace: "8:22" },
      { checkpoint: "35K", time: "3:08:12", pace: "9:15" },
      { checkpoint: "40K", time: "3:52:33", pace: "10:47" },
      { checkpoint: "Finish", time: "4:23:15", pace: "10:03" }
    ]
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Confirmed":
        return <Badge className="bg-green-100 text-green-800">Confirmed</Badge>;
      case "Pending":
        return <Badge variant="secondary">Pending Payment</Badge>;
      case "Completed":
        return <Badge className="bg-blue-100 text-blue-800">Race Completed</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1>Participant Portal</h1>
        <p className="text-muted-foreground">Welcome back, {participantInfo.name}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Registration Status */}
        <Card>
          <CardHeader>
            <CardTitle>Registration Status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-center">
              {getStatusBadge(participantInfo.status)}
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Registration ID</span>
                <span className="text-sm font-mono">{participantInfo.registrationId}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Category</span>
                <span className="text-sm font-medium">{participantInfo.category}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Start Time</span>
                <span className="text-sm font-medium">{participantInfo.startTime}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Wave Assignment</span>
                <span className="text-sm font-medium">{participantInfo.wave}</span>
              </div>
            </div>

            <div className="pt-4 border-t">
              <Button className="w-full" variant="outline">
                <Download className="mr-2 h-4 w-4" />
                Download Race Packet Info
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Bib Number */}
        <Card>
          <CardHeader>
            <CardTitle>Your Bib Number</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center space-y-4">
              <div className="bg-gray-100 border-2 border-dashed border-gray-300 rounded-lg p-8">
                <div className="text-4xl font-bold text-blue-600 mb-2">
                  {participantInfo.bibNumber}
                </div>
                <div className="text-sm text-muted-foreground">
                  {participantInfo.name}
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  {participantInfo.category}
                </div>
              </div>
              
              <div className="text-xs text-muted-foreground">
                Present this at packet pickup
              </div>
              
              <Button variant="outline" size="sm" className="w-full">
                <Download className="mr-2 h-3 w-3" />
                Save Bib Image
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Live Tracking Map Placeholder */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="h-4 w-4" />
              Live Race Tracking
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Map Placeholder */}
              <div className="bg-gray-100 border-2 border-dashed border-gray-300 rounded-lg h-48 flex items-center justify-center">
                <div className="text-center text-muted-foreground">
                  <MapPin className="h-8 w-8 mx-auto mb-2" />
                  <div className="text-sm">Live Map View</div>
                  <div className="text-xs">Track your progress on race day</div>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Current Status</span>
                  <Badge variant="secondary">Not Started</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Last Checkpoint</span>
                  <span className="text-sm">Start Line</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Estimated Finish</span>
                  <span className="text-sm">--:--:--</span>
                </div>
              </div>
              
              <Button variant="outline" size="sm" className="w-full">
                <MapPin className="mr-2 h-3 w-3" />
                Enable Live Tracking
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* My Results Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="h-4 w-4" />
            My Results
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <Trophy className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <div className="text-lg font-medium mb-2">Results will appear here after the race</div>
            <div className="text-sm">Your official time, pace, and splits will be available once you finish</div>
          </div>

          {/* Uncomment this section to show actual results */}
          {/*
          <div className="space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{raceResults.finishTime}</div>
                <div className="text-sm text-muted-foreground">Finish Time</div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-green-600">{raceResults.overallPlace}</div>
                <div className="text-sm text-muted-foreground">Overall Place</div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-purple-600">{raceResults.categoryPlace}</div>
                <div className="text-sm text-muted-foreground">Category Place</div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-orange-600">{raceResults.pace}</div>
                <div className="text-sm text-muted-foreground">Avg Pace</div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-4">Split Times</h3>
              <div className="space-y-2">
                {raceResults.splits.map((split, index) => (
                  <div key={index} className="flex justify-between items-center py-2 border-b">
                    <span className="font-medium">{split.checkpoint}</span>
                    <div className="text-right">
                      <div className="font-mono">{split.time}</div>
                      <div className="text-xs text-muted-foreground">{split.pace} pace</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex gap-4">
              <Button className="flex-1">
                <Download className="mr-2 h-4 w-4" />
                Download Certificate
              </Button>
              <Button variant="outline" className="flex-1">
                <Download className="mr-2 h-4 w-4" />
                Download Detailed Results
              </Button>
            </div>
          </div>
          */}
        </CardContent>
      </Card>
    </div>
  );
}