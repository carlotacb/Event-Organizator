import { Text, TextProps } from "./Themed";

export default function MonoText(props: TextProps) {
  const { style } = props;

  return <Text {...props} style={[style, { fontFamily: "SpaceMono" }]} />;
}
