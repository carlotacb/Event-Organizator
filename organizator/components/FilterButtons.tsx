import { Text, Pressable } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import FontAwesome from "@expo/vector-icons/FontAwesome";

const ButtonContainer = styled(Pressable)<{ color: string; active: boolean }>`
  height: 30px;
  padding: 0 15px;
  width: auto;
  border: 2px solid ${(props: { color: string }) => props.color};
  background-color: ${(props: { color: string; active: boolean }) =>
    props.active ? props.color : "transparent"};
  justify-content: center;
  align-items: center;
  border-radius: 20px;
  display: flex;
  flex-direction: row;
  gap: 10px;
  margin: 5px 3px 0;
`;

const ButtonText = styled(Text)<{ color: string; active: boolean }>`
  color: ${(props: { color: string; active: boolean }) =>
    props.active ? "white" : props.color};
  font-weight: bold;
  font-size: 13px;
`;

const InputIcon = styled(FontAwesome)`
  font-size: 13px;
`;

interface ButtonProps {
  title?: string;
  iconName?: string | never;
  onPress: () => void;
  color: string;
  active?: boolean;
}

export default function FilterButton(props: ButtonProps) {
  const { title, onPress, iconName, color, active } = props;

  return (
    <ButtonContainer onPress={onPress} color={color} active={active}>
      {iconName && (
        <InputIcon
          name={iconName}
          size={18}
          color={active ? "white" : "black"}
        />
      )}
      {title && (
        <ButtonText active={active} color={color}>
          {title}
        </ButtonText>
      )}
    </ButtonContainer>
  );
}
