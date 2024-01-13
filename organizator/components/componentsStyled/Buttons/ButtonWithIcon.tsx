import { Text, Pressable } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import FontAwesome from "@expo/vector-icons/FontAwesome";

const ButtonContainer = styled(Pressable)<{ color: string; width?: string }>`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 10px 25px;
  border-radius: 15px;
  width: ${(props: { width?: string }) => props.width || "auto"};
  background-color: ${(props: { color: string }) => props.color};
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
`;

const ButtonText = styled(Text)<{ fontSize?: string; fontBlack?: boolean }>`
  color: ${(props: { fontBlack?: boolean }) =>
    props.fontBlack ? "black" : "white"};
  font-weight: bold;
  font-size: ${(props: { fontSize?: string }) => props.fontSize || "18px"};
`;

const InputIcon = styled(FontAwesome)<{
  fontSize?: string;
  fontBlack?: boolean;
}>`
  font-size: ${(props: { fontSize?: string }) => props.fontSize || "18px"};
  color: ${(props: { fontBlack?: boolean }) =>
    props.fontBlack ? "black" : "white"};
`;

interface ButtonProps {
  title: string;
  iconName?: string | never;
  onPress: () => void;
  color: string;
  width?: string;
  fontSize?: string;
  fontBlack?: boolean;
}

export default function Button(props: ButtonProps) {
  const { title, onPress, iconName, color, width, fontSize, fontBlack } = props;

  return (
    <ButtonContainer onPress={onPress} color={color} width={width}>
      {iconName ? (
        <InputIcon
          name={iconName}
          size={18}
          color="white"
          fontSize={fontSize}
          fontBlack={fontBlack}
        />
      ) : null}
      <ButtonText fontSize={fontSize} fontBlack={fontBlack}>
        {title}
      </ButtonText>
    </ButtonContainer>
  );
}
