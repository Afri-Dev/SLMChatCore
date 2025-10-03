python test_api_complete.pyimport 'package:flutter/material.dart';
import 'faq_screen.dart';

void main() {
  runApp(const MentalHealthFaqApp());
}

class MentalHealthFaqApp extends StatelessWidget {
  const MentalHealthFaqApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mental Health FAQ',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.teal,
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
      ),
      home: const FaqScreen(),
    );
  }
}
