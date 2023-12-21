import { Text, Pressable } from "react-native";
// @ts-ignore
import styled from "styled-components/native";

const ButtonContainer = styled(Pressable)`
  height: 55px;
  width: 60%;
  background-color: darkslategray;
  margin: 10px;
  justify-content: center;
  align-items: center;
  border-radius: 20px;
`;

const ButtonText = styled(Text)`
  color: white;
  font-weight: bold;
  font-size: 18px;
`;

interface ButtonProps {
  title: string;
  onPress: () => void;
}

export default function Button(props: ButtonProps) {
  const { title, onPress } = props;

  return (
    <ButtonContainer onPress={onPress}>
      <ButtonText>{title}</ButtonText>
    </ButtonContainer>
  );
}
