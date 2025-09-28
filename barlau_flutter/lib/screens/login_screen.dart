import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:provider/provider.dart';
import 'package:feather_icons/feather_icons.dart';
import 'package:mask_text_input_formatter/mask_text_input_formatter.dart';
import '../providers/auth_provider.dart';
import '../services/biometric_service.dart';
import 'main_screen.dart';
import 'quick_login_screen.dart';
import 'pin_setup_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen>
    with TickerProviderStateMixin {
  final _phoneController = TextEditingController();
  final _passwordController = TextEditingController();
  final _phoneFocusNode = FocusNode();
  final _passwordFocusNode = FocusNode();
  bool _isPasswordVisible = false;
  bool _isLoading = false;
  bool _isNavigating = false; // Флаг для предотвращения множественной навигации

  // Маска для номера телефона в формате +7 (111) 111-1111
  final _phoneMaskFormatter = MaskTextInputFormatter(
    mask: '+7 (###) ###-####',
    filter: {"#": RegExp(r'[0-9]')},
  );

  late AnimationController _logoController;
  late AnimationController _formController;
  late AnimationController _titleController;
  late AnimationController _subtitleController;
  late AnimationController _phoneBorderController;
  late AnimationController _passwordBorderController;

  late Animation<double> _logoAnimation;
  late Animation<double> _formAnimation;
  late Animation<double> _titleAnimation;
  late Animation<double> _subtitleAnimation;
  late Animation<double> _phoneBorderAnimation;
  late Animation<double> _passwordBorderAnimation;

  @override
  void initState() {
    super.initState();

    // Добавляем слушатели фокуса для полей
    _phoneFocusNode.addListener(() {
      if (_phoneFocusNode.hasFocus) {
        _phoneBorderController.forward();
      } else {
        _phoneBorderController.reverse();
      }
      setState(() {});
    });
    _passwordFocusNode.addListener(() {
      if (_passwordFocusNode.hasFocus) {
        _passwordBorderController.forward();
      } else {
        _passwordBorderController.reverse();
      }
      setState(() {});
    });
    
    // Проверяем быстрый вход
    _checkQuickLogin();
    
    // Если пользователь уже авторизован, сразу переходим к PIN настройке
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkIfAlreadyAuthenticated();
    });

    // Контроллеры анимации
    _logoController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _formController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _titleController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    _subtitleController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    _phoneBorderController = AnimationController(
      duration: const Duration(milliseconds: 200),
      vsync: this,
    );
    _passwordBorderController = AnimationController(
      duration: const Duration(milliseconds: 200),
      vsync: this,
    );

    // Анимации
    _logoAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _logoController, curve: Curves.easeOutBack),
    );
    _formAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _formController, curve: Curves.easeOut),
    );
    _titleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _titleController, curve: Curves.easeOut),
    );
    _subtitleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _subtitleController, curve: Curves.easeOut),
    );
    _phoneBorderAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _phoneBorderController, curve: Curves.easeInOut),
    );
    _passwordBorderAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _passwordBorderController, curve: Curves.easeInOut),
    );

    // Запуск анимаций
    _startAnimations();
  }

  void _startAnimations() async {
    if (!mounted) return;
    
    await Future.delayed(const Duration(milliseconds: 300));
    if (!mounted) return;
    _logoController.forward();
    
    await Future.delayed(const Duration(milliseconds: 200));
    if (!mounted) return;
    _formController.forward();
    
    await Future.delayed(const Duration(milliseconds: 100));
    if (!mounted) return;
    _titleController.forward();
    
    await Future.delayed(const Duration(milliseconds: 100));
    if (!mounted) return;
    _subtitleController.forward();
  }

  Future<void> _checkQuickLogin() async {
    try {
      final isQuickLoginEnabled = await BiometricService.isQuickLoginEnabled();
      if (isQuickLoginEnabled && mounted) {
        // Переходим на экран быстрого входа
        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(
            builder: (context) => const QuickLoginScreen(),
            fullscreenDialog: true, // Открываем как полноэкранный модальный экран
          ),
          (route) => false,
        );
      }
    } catch (e) {
      print('LoginScreen: Ошибка проверки быстрого входа: $e');
    }
  }

  void _checkIfAlreadyAuthenticated() async {
    try {
      final authProvider = context.read<AuthProvider>();
      if (authProvider.isAuthenticated && mounted && !_isNavigating) {
        print('🎬 LoginScreen: Пользователь уже авторизован, переходим в приложение');
        _isNavigating = true;
        
        // Проверяем, настроен ли быстрый вход
        final isQuickLoginEnabled = await BiometricService.isQuickLoginEnabled();
        if (isQuickLoginEnabled) {
          // Если быстрый вход настроен, переходим к нему
          Navigator.of(context).pushAndRemoveUntil(
            MaterialPageRoute(
              builder: (context) => const QuickLoginScreen(),
              fullscreenDialog: true,
            ),
            (route) => false,
          );
        } else {
          // Если быстрый вход не настроен, переходим в приложение
          Navigator.of(context).pushAndRemoveUntil(
            MaterialPageRoute(builder: (context) => const MainScreen()),
            (route) => false,
          );
        }
      }
    } catch (e) {
      print('🔴 Ошибка проверки авторизации: $e');
    }
  }

  @override
  void dispose() {
    _phoneController.dispose();
    _passwordController.dispose();
    _phoneFocusNode.dispose();
    _passwordFocusNode.dispose();
    _logoController.dispose();
    _formController.dispose();
    _titleController.dispose();
    _subtitleController.dispose();
    _phoneBorderController.dispose();
    _passwordBorderController.dispose();
    _isNavigating = false; // Сбрасываем флаг навигации
    super.dispose();
  }

  Future<void> _login() async {
    // Получаем номер телефона и конвертируем его в формат +7XXXXXXXXXX
    final maskedPhone = _phoneController.text.trim();
    final password = _passwordController.text.trim();
    
    // Извлекаем только цифры из маскированного номера (должно быть 11 цифр: 7 + 10 цифр номера)
    final phoneDigits = maskedPhone.replaceAll(RegExp(r'[^\d]'), '');
    final phone = '+$phoneDigits';
    
    // Проверяем, что номер телефона содержит 11 цифр (7 + 10 цифр номера)
    if (phoneDigits.length != 11 || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Пожалуйста, заполните все поля корректно'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      print('LoginScreen: Начинаем авторизацию...');
      print('LoginScreen: username: $phone, password: $password');
      
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      
      // Используем реальные данные для авторизации
      final username = phone;
      final userPassword = password;
      
      print('LoginScreen: Вызываем authProvider.login...');
      final success = await authProvider.login(
        username,
        userPassword,
        context: context,
      );
      print('LoginScreen: Результат авторизации: $success');

      if (success && mounted) {
        // Успешная авторизация - проверяем, нужно ли настроить быстрый вход
        final now = DateTime.now();
        print('✅ Успешная авторизация в ${now.millisecondsSinceEpoch}');
        
        // Очищаем старые данные быстрого входа для первого входа
        try {
          await BiometricService.clearQuickLoginData();
        } catch (_) {}
        
        // Всегда переходим к настройке PIN с анимацией при первом входе
        final userData = authProvider.getUserDataForQuickLogin();
        if (userData != null && !_isNavigating) {
          print('🎬 LoginScreen: Переходим к PIN настройке с анимацией');
          _isNavigating = true;
          
          // Небольшая задержка для плавности
          await Future.delayed(const Duration(milliseconds: 100));
          
          // Навигация с анимацией
          Navigator.of(context).pushReplacement(
            PageRouteBuilder(
              pageBuilder: (context, animation, secondaryAnimation) {
                return PinSetupScreen(
                  username: userData['username'] ?? '',
                  password: '',
                  displayName: userData['displayName'],
                  firstName: userData['firstName'],
                  isExistingSetup: false,
                );
              },
              transitionDuration: const Duration(milliseconds: 500),
              transitionsBuilder: (context, animation, secondaryAnimation, child) {
                // Плавная анимация slide справа налево
                return SlideTransition(
                  position: Tween<Offset>(
                    begin: const Offset(1.0, 0.0),
                    end: Offset.zero,
                  ).animate(CurvedAnimation(
                    parent: animation,
                    curve: Curves.easeOutCubic,
                  )),
                  child: FadeTransition(
                    opacity: Tween<double>(
                      begin: 0.0,
                      end: 1.0,
                    ).animate(CurvedAnimation(
                      parent: animation,
                      curve: Curves.easeOut,
                    )),
                    child: child,
                  ),
                );
              },
            ),
          );
          return;
        }
        
        final now2 = DateTime.now();
        print('✅ Авторизация успешна, AuthWrapper покажет нужный экран в ${now2.millisecondsSinceEpoch}');
        
      } else if (!success && mounted) {
        // Получаем конкретную ошибку из AuthProvider
        final errorMessage = authProvider.error ?? 'Неверный логин или пароль';
        
        // Показываем минималистичное уведомление об ошибке
        showDialog(
          context: context,
          barrierDismissible: true,
          builder: (BuildContext context) {
            return Dialog(
              backgroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
              ),
              child: Container(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Иконка ошибки
                    Container(
                      width: 48,
                      height: 48,
                      decoration: BoxDecoration(
                        color: const Color(0xFFFEE2E2),
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: const Icon(
                        Icons.error_outline,
                        color: Color(0xFFDC2626),
                        size: 24,
                      ),
                    ),
                    const SizedBox(height: 16),
                    
                    // Заголовок
                    const Text(
                      'Ошибка входа',
                      style: TextStyle(
                        fontFamily: 'InterTight',
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF1F2937),
                      ),
                    ),
                    const SizedBox(height: 8),
                    
                    // Сообщение
                    Text(
                      errorMessage,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontFamily: 'InterTight',
                        fontSize: 14,
                        color: Color(0xFF6B7280),
                        height: 1.4,
                      ),
                    ),
                    const SizedBox(height: 24),
                    
                    // Кнопка
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () => Navigator.of(context).pop(),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF2679DB),
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                          elevation: 0,
                        ),
                        child: const Text(
                          'Понятно',
                          style: TextStyle(
                            fontFamily: 'InterTight',
                            fontSize: 16,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Ошибка подключения к серверу: $e'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 3),
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final now = DateTime.now();
    print('🔴 LoginScreen: build вызван, показываем экран в ${now.millisecondsSinceEpoch}');
    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          color: Colors.white, // Простой белый фон
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            child: Column(
              children: [
                // Логотип сверху
                Padding(
                  padding: const EdgeInsets.only(top: 20),
                  child: AnimatedBuilder(
                    animation: _logoAnimation,
                    builder: (context, child) {
                      return Transform.translate(
                        offset: Offset(0, -10 * (1 - _logoAnimation.value)),
                        child: Opacity(
                          opacity: _logoAnimation.value.clamp(0.0, 1.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Image.asset(
                                'assets/images/logo.png',
                                width: 56,
                                height: 30,
                              ),
                              const SizedBox(width: 8),
                              const Text(
                                'Barlau.kz',
                                style: TextStyle(
                                  fontSize: 24,
                                  fontWeight: FontWeight.w600,
                                  color: Color(0xFF000000),
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),

                // Пространство
                const SizedBox(height: 30),

                // Форма в центре
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 32),
                  child: AnimatedBuilder(
                    animation: _formAnimation,
                    builder: (context, child) {
                      return Transform.translate(
                        offset: Offset(0, 10 * (1 - _formAnimation.value)),
                        child: Opacity(
                          opacity: _formAnimation.value.clamp(0.0, 1.0),
                          child: Container(
                            constraints: const BoxConstraints(maxWidth: 440),
                            margin: EdgeInsets.symmetric(
                              horizontal: MediaQuery.of(context).size.width > 440 
                                  ? (MediaQuery.of(context).size.width - 440) / 2 
                                  : 0,
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.center,
                              mainAxisSize: MainAxisSize.min,
                              children: [

                                // Поле телефона
                                AnimatedBuilder(
                                  animation: _phoneBorderAnimation,
                                  builder: (context, child) {
                                    return Container(
                                      decoration: BoxDecoration(
                                        color: Colors.white,
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(
                                          color: Color.lerp(
                                            const Color(0xFFE5E7EB), // border-gray-200
                                            const Color(0xFF2679DB), // Акцентный синий цвет
                                            _phoneBorderAnimation.value,
                                          )!,
                                          width: 1,
                                        ),
                                      ),
                                      child: TextField(
                                        controller: _phoneController,
                                        focusNode: _phoneFocusNode,
                                        inputFormatters: [_phoneMaskFormatter],
                                        keyboardType: TextInputType.phone,
                                        textInputAction: TextInputAction.next,
                                        onChanged: (value) {
                                          // Применяем маску к введенному тексту
                                          final maskedValue = _phoneMaskFormatter.maskText(value);
                                          if (maskedValue != value) {
                                            _phoneController.value = TextEditingValue(
                                              text: maskedValue,
                                              selection: TextSelection.collapsed(offset: maskedValue.length),
                                            );
                                          }
                                        },
                                        style: const TextStyle(
                                          fontSize: 16,
                                          color: Color(0xFF18181B),
                                        ),
                                        decoration: InputDecoration(
                                          hintText: _phoneFocusNode.hasFocus || _phoneController.text.isNotEmpty ? '+7 (___) ___-____' : 'Телефон',
                                          hintStyle: const TextStyle(
                                            color: Color(0xFF9CA3AF), // text-gray-400
                                          ),
                                          border: InputBorder.none,
                                          contentPadding: const EdgeInsets.symmetric(
                                            horizontal: 16,
                                            vertical: 12,
                                          ),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                                const SizedBox(height: 12),

                                // Поле пароля
                                AnimatedBuilder(
                                  animation: _passwordBorderAnimation,
                                  builder: (context, child) {
                                    return Container(
                                      decoration: BoxDecoration(
                                        color: Colors.white,
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(
                                          color: Color.lerp(
                                            const Color(0xFFE5E7EB), // border-gray-200
                                            const Color(0xFF2679DB), // Акцентный синий цвет
                                            _passwordBorderAnimation.value,
                                          )!,
                                          width: 1,
                                        ),
                                      ),
                                      child: TextField(
                                        controller: _passwordController,
                                        focusNode: _passwordFocusNode,
                                        obscureText: !_isPasswordVisible,
                                        keyboardType: TextInputType.text,
                                        textInputAction: TextInputAction.done,
                                        style: const TextStyle(
                                          fontSize: 16,
                                          color: Color(0xFF18181B),
                                        ),
                                        decoration: InputDecoration(
                                          hintText: 'Пароль',
                                          hintStyle: const TextStyle(
                                            color: Color(0xFF9CA3AF), // text-gray-400
                                          ),
                                          border: InputBorder.none,
                                          contentPadding: const EdgeInsets.symmetric(
                                            horizontal: 16,
                                            vertical: 12,
                                          ),
                                          suffixIcon: IconButton(
                                            icon: Icon(
                                              _isPasswordVisible
                                                  ? FeatherIcons.eyeOff
                                                  : FeatherIcons.eye,
                                              color: const Color(0xFF6B7280),
                                              size: 20,
                                            ),
                                            onPressed: () {
                                              setState(() {
                                                _isPasswordVisible = !_isPasswordVisible;
                                              });
                                            },
                                          ),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                                const SizedBox(height: 12),

                                // Кнопка входа
                                SizedBox(
                                  width: double.infinity,
                                  child: ElevatedButton(
                                    onPressed: _isLoading ? null : _login,
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: const Color(0xFF2679DB), // bg-blue-600
                                      foregroundColor: Colors.white,
                                      padding: const EdgeInsets.symmetric(vertical: 12),
                                      shape: RoundedRectangleBorder(
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      elevation: 0,
                                      disabledBackgroundColor: const Color(0xFF9CA3AF),
                                    ),
                                    child: _isLoading
                                        ? const SizedBox(
                                            height: 20,
                                            width: 20,
                                            child: CircularProgressIndicator(
                                              strokeWidth: 2,
                                              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                                            ),
                                          )
                                        : const Text(
                                            'Войти',
                                            style: TextStyle(
                                              fontSize: 16,
                                              fontWeight: FontWeight.w600,
                                            ),
                                          ),
                                  ),
                                ),

                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ),

                // Пространство внизу
                const SizedBox(height: 100),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
 
 
 
 