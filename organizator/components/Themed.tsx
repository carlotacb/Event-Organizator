/**
 * Learn more about Light and Dark modes:
 * https://docs.expo.io/guides/color-schemes/
 */

import {
  Text as DefaultText,
  useColorScheme,
  View as DefaultView,
  ScrollView as DefaultScrollView,
} from "react-native";

import Colors from "../constants/Colors";

type ThemeProps = {
  lightColor?: string | null;
  darkColor?: string | null;
};

export type TextProps = ThemeProps & DefaultText["props"];
export type ViewProps = ThemeProps & DefaultView["props"];

export function useThemeColor(
  props: { light?: string; dark?: string },
  colorName: keyof typeof Colors.light & keyof typeof Colors.dark,
) {
  const theme = useColorScheme() ?? "light";
  const colorFromProps = props[theme];

  if (colorFromProps) {
    return colorFromProps;
  }
  return Colors[theme][colorName];
}

export function Text(props: TextProps) {
  const { style, lightColor, darkColor, ...otherProps } = props;

  const lightColorDefinition: string = lightColor || "#FFF";
  const darkColorDefinition: string = darkColor || "#000";

  const color = useThemeColor(
    { light: lightColorDefinition, dark: darkColorDefinition },
    "text",
  );

  return <DefaultText style={[{ color }, style]} {...otherProps} />;
}

export function View(props: ViewProps) {
  const { style, lightColor, darkColor, ...otherProps } = props;

  const lightColorDefinition: string = lightColor || "#FFF";
  const darkColorDefinition: string = darkColor || "#000";

  const backgroundColor = useThemeColor(
    { light: lightColorDefinition, dark: darkColorDefinition },
    "background",
  );

  return <DefaultView style={[{ backgroundColor }, style]} {...otherProps} />;
}

export function ScreenScrollView(props: ViewProps) {}
