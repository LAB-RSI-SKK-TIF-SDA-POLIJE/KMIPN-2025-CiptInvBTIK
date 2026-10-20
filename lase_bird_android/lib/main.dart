import 'package:flutter/material.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bird Laser IoT',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepOrange),
        useMaterial3: true,
      ),
      home: const VideoStreamScreen(),
    );
  }
}

class VideoStreamScreen extends StatefulWidget {
  const VideoStreamScreen({super.key});

  @override
  State<VideoStreamScreen> createState() => _VideoStreamScreenState();
}

class _VideoStreamScreenState extends State<VideoStreamScreen> {
  // GANTI DENGAN IP RASPBERRY PI ANDA ATAU URL TUNNEL/NGROK
  String streamUrl = 'http://192.168.1.50:5000/video_feed';
  bool isRunning = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bird Laser IoT - Monitoring'),
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: Icon(isRunning ? Icons.pause : Icons.play_arrow),
            onPressed: () {
              setState(() {
                isRunning = !isRunning;
              });
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              setState(() {
                isRunning = false;
              });
              Future.delayed(const Duration(milliseconds: 200), () {
                setState(() {
                  isRunning = true;
                });
              });
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: Container(
              color: Colors.black,
              child: Center(
                child: isRunning
                    ? Mjpeg(
                        isLive: true,
                        stream: streamUrl,
                        error: (context, error, stack) {
                          return Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(
                                Icons.error_outline,
                                color: Colors.red,
                                size: 48,
                              ),
                              const SizedBox(height: 12),
                              Text(
                                'Gagal terhubung ke RPi:\n$streamUrl',
                                textAlign: TextAlign.center,
                                style: const TextStyle(color: Colors.white),
                              ),
                              const SizedBox(height: 12),
                              ElevatedButton(
                                onPressed: () {
                                  setState(() {
                                    isRunning = false;
                                  });
                                  Future.delayed(
                                    const Duration(milliseconds: 300),
                                    () {
                                      setState(() {
                                        isRunning = true;
                                      });
                                    },
                                  );
                                },
                                child: const Text('Coba Hubungkan Lagi'),
                              ),
                            ],
                          );
                        },
                        loading: (context) => const Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            CircularProgressIndicator(color: Colors.orange),
                            SizedBox(height: 12),
                            Text(
                              'Menghubungkan ke Stream RPi...',
                              style: TextStyle(color: Colors.white),
                            ),
                          ],
                        ),
                      )
                    : const Center(
                        child: Text(
                          'Stream Dihentikan',
                          style: TextStyle(color: Colors.white),
                        ),
                      ),
              ),
            ),
          ),
          Container(
            padding: const EdgeInsets.all(16.0),
            color: Colors.grey[900],
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(
                  children: [
                    Icon(Icons.circle, color: Colors.green, size: 12),
                    SizedBox(width: 8),
                    Text(
                      'Status: Live YOLOv8',
                      style: TextStyle(color: Colors.white),
                    ),
                  ],
                ),
                Text(
                  'RPi 5 Target System',
                  style: TextStyle(color: Colors.grey[400], fontSize: 12),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
