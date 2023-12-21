import { Text, StyleSheet, Pressable } from "react-native";

interface ButtonProps {
  title: string;
  onPress: () => void;
}

export default function Button(props: ButtonProps) {
  const { title, onPress } = props;

  return (
    <Pressable onPress={onPress} style={styles.button}>
      <Text style={styles.title}>{title}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    height: 55,
    width: "100%",
    backgroundColor: "blue",
    marginVertical: 10,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 100,
  },
  title: {
    color: "white",
    fontWeight: "bold",
    fontSize: 18,
  },
});
