import { Head } from "expo-head";
import { Stack } from "expo-router";
import { ScrollView, StyleSheet } from "react-native";

import { ExternalLink } from "../components/ExternalLink";
import { MonoText } from "../components/StyledText";
import { View } from "../components/Themed";
import Colors from "../constants/Colors";

export default function HomePage() {
  return (
    <>
      <Head>
        <title>Homepage</title>
      </Head>
      <ScrollView>
        <View style={styles.container}>
          <Stack.Screen options={{ headerShown: false }} />
          <MonoText style={styles.title}>
            This will be the home page for the application
          </MonoText>

          <View style={styles.helpContainer}>
            <ExternalLink
              style={styles.helpLink}
              href="https://docs.expo.io/get-started/create-a-new-app/#opening-the-app-on-your-phonetablet"
            >
              <MonoText
                style={styles.helpLinkText}
                lightColor={Colors.light.tint}
              >
                Tap here if your app doesn't automatically update after making
                changes
              </MonoText>
            </ExternalLink>
          </View>

          <MonoText>Lorem ipsum dolor sit amet,</MonoText>
        </View>
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    paddingLeft: "20%",
    paddingRight: "20%",
    paddingTop: "5%",
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
  },
  helpContainer: {
    marginTop: 15,
    marginHorizontal: 20,
    alignItems: "center",
  },
  helpLink: {
    paddingVertical: 15,
  },
  helpLinkText: {
    textAlign: "center",
  },
});
