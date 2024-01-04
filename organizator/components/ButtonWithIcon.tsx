import { Text, Pressable } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import FontAwesome from "@expo/vector-icons/FontAwesome";

const ButtonContainer = styled(Pressable)<{ color: string }>`
  height: 55px;
  padding: 0 30px;
  width: auto;
  background-color: ${(props: { color: string }) => props.color};
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
  margin: 10px;
  justify-content: center;
  align-items: center;
  border-radius: 20px;
  display: flex;
  flex-direction: row;
  gap: 10px;
`;

const ButtonText = styled(Text)`
  color: white;
  font-weight: bold;
  font-size: 18px;
`;

const InputIcon = styled(FontAwesome)`
  font-size: 18px;
`;

interface ButtonProps {
  title: string;
  iconName: string | never;
  onPress: () => void;
  color: string;
}

export default function Button(props: ButtonProps) {
  const { title, onPress, iconName, color } = props;

  return (
    <ButtonContainer onPress={onPress} color={color}>
      <InputIcon name={iconName} size={18} color="white" />
      <ButtonText>{title}</ButtonText>
    </ButtonContainer>
  );
}
