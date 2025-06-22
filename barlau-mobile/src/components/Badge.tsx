import React from 'react';
import { Text, StyleSheet, TextStyle } from 'react-native';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'secondary' | 'destructive' | 'outline';
  style?: TextStyle;
}

const Badge: React.FC<BadgeProps> = ({ children, variant = 'default', style }) => {
  return (
    <Text style={[styles.badge, styles[variant], style]}>
      {children}
    </Text>
  );
};

const styles = StyleSheet.create({
  badge: {
    fontSize: 12,
    fontWeight: '500',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 16,
    overflow: 'hidden',
    textAlign: 'center',
    letterSpacing: -0.025,
  },
  default: {
    backgroundColor: '#020817',
    color: '#F8FAFC',
  },
  secondary: {
    backgroundColor: '#F1F5F9',
    color: '#0F172A',
  },
  destructive: {
    backgroundColor: '#DC2626',
    color: '#F8FAFC',
  },
  outline: {
    backgroundColor: 'transparent',
    color: '#020817',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
});

export default Badge; 