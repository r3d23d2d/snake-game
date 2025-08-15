import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Check, ArrowRight, Star, DollarSign, Clock, Zap } from 'lucide-react';

const Pricing = ({ data, onOpenForm }) => {
  return (
    <section id="pricing" className="py-20 bg-gradient-to-br from-cyan-50 via-white to-sky-50 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-200/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-sky-300/15 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="text-center mb-16 animate-fade-in-up">
          <Badge className="bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 px-4 py-2 text-sm mb-4 shadow-sm hover:shadow-md transition-all duration-300 hover:scale-105">
            <DollarSign className="w-4 h-4 mr-2" />
            Прозрачное ценообразование
          </Badge>
          <h2 className="text-3xl lg:text-5xl font-bold bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent mb-6">
            Стоимость услуг
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Фиксированная стоимость без скрытых платежей. 
            Вы платите за результат, а не за эксперименты.
          </p>
        </div>

        <div className="max-w-4xl mx-auto animate-fade-in-up delay-200">
          <Card className="shadow-2xl border-0 overflow-hidden hover:shadow-3xl transition-all duration-500 bg-white/90 backdrop-blur-sm">
            {/* Header */}
            <div className="bg-gradient-to-r from-cyan-600 to-sky-600 text-white p-8 text-center relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
              <div className="absolute bottom-0 left-0 w-24 h-24 bg-cyan-400/20 rounded-full translate-y-12 -translate-x-12"></div>
              <div className="relative z-10">
                <div className="flex items-center justify-center mb-4">
                  <Star className="h-8 w-8 text-yellow-300 mr-2 animate-spin-slow" />
                  <h3 className="text-3xl font-bold">Комплексное продвижение</h3>
                  <Star className="h-8 w-8 text-yellow-300 ml-2 animate-spin-slow" />
                </div>
                <p className="text-xl text-cyan-100">
                  Всё необходимое для успешной рекламы стоматологии
                </p>
              </div>
            </div>

            <CardContent className="p-8">
              <div className="grid lg:grid-cols-2 gap-8">
                {/* Pricing */}
                <div className="space-y-6">
                  <div>
                    <h4 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                      <DollarSign className="w-6 h-6 mr-2 text-cyan-600" />
                      Стоимость
                    </h4>
                    
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-4 bg-gradient-to-r from-cyan-50 to-sky-50 rounded-lg hover:shadow-md transition-all duration-300 hover:scale-105 group">
                        <span className="text-gray-700 font-medium group-hover:text-cyan-700 transition-colors">Настройка (разовая)</span>
                        <span className="text-2xl font-bold bg-gradient-to-r from-cyan-600 to-sky-600 bg-clip-text text-transparent group-hover:scale-110 transition-transform">
                          {data.setup_fee.toLocaleString()}₽
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg hover:shadow-md transition-all duration-300 hover:scale-105 group">
                        <span className="text-gray-700 font-medium group-hover:text-green-700 transition-colors">Ведение (ежемесячно)</span>
                        <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent group-hover:scale-110 transition-transform">
                          {data.monthly_fee.toLocaleString()}₽
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-violet-50 rounded-lg hover:shadow-md transition-all duration-300 hover:scale-105 group">
                        <span className="text-gray-700 font-medium group-hover:text-purple-700 transition-colors">Мин. рекламный бюджет</span>
                        <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-violet-600 bg-clip-text text-transparent group-hover:scale-110 transition-transform">
                          {data.min_budget.toLocaleString()}₽
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gradient-to-r from-yellow-50 to-amber-50 border-2 border-yellow-200 rounded-lg p-4 hover:shadow-md transition-all duration-300 hover:scale-105 group">
                    <div className="flex items-center mb-2">
                      <Star className="h-5 w-5 text-yellow-600 mr-2 group-hover:animate-spin transition-all" />
                      <span className="font-semibold text-yellow-800">Специальное предложение</span>
                    </div>
                    <p className="text-yellow-700 text-sm">
                      При заключении договора до конца месяца — скидка 20% на настройку
                    </p>
                  </div>
                </div>

                {/* What's included */}
                <div>
                  <h4 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                    <Zap className="w-6 h-6 mr-2 text-cyan-600" />
                    Что входит в стоимость
                  </h4>
                  
                  <div className="space-y-3">
                    {data.includes.map((item, index) => (
                      <div 
                        key={index} 
                        className="flex items-start hover:bg-cyan-50 rounded-lg p-2 transition-all duration-300 hover:scale-105 group"
                        style={{ animationDelay: `${index * 100}ms` }}
                      >
                        <div className="w-6 h-6 bg-gradient-to-br from-green-100 to-emerald-200 rounded-full flex items-center justify-center mr-3 mt-0.5 shadow-sm group-hover:shadow-md group-hover:scale-110 transition-all duration-300">
                          <Check className="h-4 w-4 text-green-600" />
                        </div>
                        <span className="text-gray-700 group-hover:text-cyan-700 transition-colors">{item}</span>
                      </div>
                    ))}
                  </div>

                  <div className="mt-8 p-6 bg-gradient-to-r from-cyan-50 to-sky-50 rounded-lg hover:shadow-md transition-all duration-300 hover:scale-105 group">
                    <h5 className="font-bold text-gray-900 mb-3 flex items-center group-hover:text-cyan-700 transition-colors">
                      <Clock className="w-5 h-5 mr-2 text-cyan-600 group-hover:animate-spin" />
                      Результат за первый месяц:
                    </h5>
                    <ul className="text-sm text-gray-700 space-y-2">
                      {[
                        "Стоимость заявки от 350₽",
                        "Конверсия 8-12%",
                        "Первые заявки через 3-5 дней",
                        "Полная настройка всех кампаний"
                      ].map((item, index) => (
                        <li key={index} className="flex items-center group-hover:text-cyan-700 transition-colors">
                          <div className="w-2 h-2 bg-cyan-500 rounded-full mr-2 animate-pulse"></div>
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              {/* CTA */}
              <div className="mt-8 text-center">
                <Button 
                  onClick={onOpenForm}
                  size="lg"
                  className="bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-700 hover:to-sky-700 text-white px-12 py-4 text-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 hover:scale-105 group relative overflow-hidden"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-sky-500 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
                  <span className="relative">Начать сотрудничество</span>
                  <ArrowRight className="ml-2 h-6 w-6 group-hover:translate-x-1 transition-transform relative" />
                </Button>
                
                <p className="mt-4 text-gray-600 text-lg">
                  Бесплатная консультация • Расчет стоимости заявки • План продвижения
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Additional info */}
        <div className="mt-16 text-center animate-fade-in-up delay-400">
          <div className="max-w-4xl mx-auto">
            <h3 className="text-2xl font-bold bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent mb-8">
              Почему такая стоимость?
            </h3>
            
            <div className="grid md:grid-cols-3 gap-8">
              {[
                { 
                  title: "Узкая специализация", 
                  desc: "Работаю только со стоматологиями — знаю все нюансы ниши",
                  color: "from-cyan-600 to-sky-600",
                  delay: "0ms"
                },
                { 
                  title: "Проверенные методы", 
                  desc: "Использую только работающие стратегии с доказанной эффективностью",
                  color: "from-green-600 to-emerald-600",
                  delay: "200ms"
                },
                { 
                  title: "Личная работа", 
                  desc: "Все кампании настраиваю лично, без привлечения сторонних специалистов",
                  color: "from-purple-600 to-violet-600",
                  delay: "400ms"
                }
              ].map((item, index) => (
                <div 
                  key={index}
                  className="text-center group animate-fade-in-up"
                  style={{ animationDelay: item.delay }}
                >
                  <div className={`w-12 h-12 bg-gradient-to-br ${item.color.replace('600', '100')} rounded-lg flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:shadow-xl group-hover:scale-110 transition-all duration-300`}>
                    <span className={`font-bold text-lg bg-gradient-to-r ${item.color} bg-clip-text text-transparent`}>
                      {index + 1}
                    </span>
                  </div>
                  <h4 className="font-bold text-gray-900 mb-2 group-hover:text-cyan-700 transition-colors">{item.title}</h4>
                  <p className="text-gray-600 text-sm leading-relaxed group-hover:text-cyan-600 transition-colors">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Pricing;