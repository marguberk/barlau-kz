import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';

interface ButtonProps {
  children: React.ReactNode;
  onPress?: () => void;
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  disabled?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

const Button: React.FC<ButtonProps> = ({ 
  children, 
  onPress, 
  variant = 'default', 
  size = 'default',
  disabled = false,
  style,
  textStyle 
}) => {
  return (
    <TouchableOpacity
      style={[
        styles.button,
        styles[`${variant}Button`],
        styles[`${size}Size`],
        disabled && styles.disabled,
        style
      ]}
      onPress={onPress}
      disabled={disabled}
      activeOpacity={0.8}
    >
      <Text style={[
        styles.text,
        styles[`${variant}Text`],
        styles[`${size}TextSize`],
        disabled && styles.disabledText,
        textStyle
      ]}>
        {children}
      </Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    borderRadius: 6,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  text: {
    fontWeight: '500',
    letterSpacing: -0.025,
  },
  
  // Variants
  defaultButton: {
    backgroundColor: '#2563EB',
  },
  destructiveButton: {
    backgroundColor: '#DC2626',
  },
  outlineButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  secondaryButton: {
    backgroundColor: '#F1F5F9',
  },
  ghostButton: {
    backgroundColor: 'transparent',
    shadowOpacity: 0,
    elevation: 0,
  },
  linkButton: {
    backgroundColor: 'transparent',
    shadowOpacity: 0,
    elevation: 0,
  },
  
  // Text variants
  defaultText: {
    color: '#F8FAFC',
  },
  destructiveText: {
    color: '#F8FAFC',
  },
  outlineText: {
    color: '#020817',
  },
  secondaryText: {
    color: '#0F172A',
  },
  ghostText: {
    color: '#020817',
  },
  linkText: {
    color: '#020817',
    textDecorationLine: 'underline',
  },
  
  // Sizes
  defaultSize: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    minHeight: 40,
  },
  smSize: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    minHeight: 32,
  },
  lgSize: {
    paddingHorizontal: 24,
    paddingVertical: 12,
    minHeight: 48,
  },
  iconSize: {
    width: 40,
    height: 40,
    paddingHorizontal: 0,
    paddingVertical: 0,
  },
  
  // Text sizes
  defaultTextSize: {
    fontSize: 14,
  },
  smTextSize: {
    fontSize: 12,
  },
  lgTextSize: {
    fontSize: 16,
  },
  iconTextSize: {
    fontSize: 14,
  },
  
  // Disabled
  disabled: {
    opacity: 0.5,
  },
  disabledText: {
    opacity: 0.5,
  },
});

export default Button; 