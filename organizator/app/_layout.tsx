import React from "react";
import { Stack, useRouter } from "expo-router";
import { Button } from "react-native";

const RootLayout = () => {
  const router = useRouter();

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
          headerRight: () => (
            <Button onPress={() => router.push("modal")} title="Open" />
          ),
        }}
      />
      <Stack.Screen
        name="modal"
        options={{
          presentation: "modal",
          headerLeft: () => (
            <Button onPress={() => router.back()} title="Close" />
          ),
        }}
      />
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="(tabs2)" options={{ headerShown: false }} />
    </Stack>
  );
};

export default RootLayout;
