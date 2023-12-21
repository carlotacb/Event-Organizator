import React from "react";
import { Stack } from "expo-router";

export default function RootLayout() {
  // const router = useRouter();

  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: "#10101E" },
        headerTintColor: "#FFF",
        headerTitleStyle: { fontWeight: "bold" },
      }}
    >
      <Stack.Screen
        name="index"
        options={{ headerTitle: "Login", headerShown: false }}
      />
      <Stack.Screen
        name="register"
        options={{
          headerTitle: "Create account",
        }}
      />
      <Stack.Screen
        name="modal"
        options={{
          presentation: "modal",
          // headerLeft: () => (
          //  <Button onPress={() => router.back()} title="Close" />
          // ),
        }}
      />
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="(tabs2)" options={{ headerShown: false }} />
    </Stack>
  );
}
