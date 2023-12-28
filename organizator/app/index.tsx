import { Pressable, StyleSheet, Text, View } from "react-native";
import { Link, useRouter } from "expo-router";

export default function Page() {
  const router = useRouter();

  const handlePress = () => {
    router.replace("/home");
  };

  return (
    <View style={styles.container}>
      <View style={styles.main}>
        <Text style={styles.title}>Hello World</Text>
        <Text style={styles.subtitle}>This is the first page of your app.</Text>
        <Link href="/register" asChild>
          <Pressable>
            <Text style={{ padding: 20, fontSize: 20 }}>Register</Text>
          </Pressable>
        </Link>
        <Link href="/login" asChild>
          <Pressable>
            <Text style={{ padding: 20, fontSize: 20 }}>Login</Text>
          </Pressable>
        </Link>
        <Pressable onPress={handlePress}>
          <Text style={{ padding: 20, fontSize: 20 }}>Home</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    padding: 24,
  },
  main: {
    flex: 1,
    justifyContent: "center",
    maxWidth: 960,
    marginHorizontal: "auto",
  },
  title: {
    fontSize: 64,
    fontWeight: "bold",
  },
  subtitle: {
    fontSize: 36,
    color: "#38434D",
  },
});
