import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Check, ArrowRight, Star } from 'lucide-react';

const Pricing = ({ data, onOpenForm }) => {
  return (
    <section id="pricing" className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="bg-green-100 text-green-800 px-4 py-2 text-sm mb-4">
            Прозрачное ценообразование
          </Badge>
          <h2 className="text-3xl lg:text-5xl font-bold text-gray-900 mb-6">
            Стоимость услуг
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Фиксированная стоимость без скрытых платежей. 
            Вы платите за результат, а не за эксперименты.
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <Card className="shadow-2xl border-0 overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-8 text-center">
              <div className="flex items-center justify-center mb-4">
                <Star className="h-8 w-8 text-yellow-300 mr-2" />
                <h3 className="text-3xl font-bold">Комплексное продвижение</h3>
                <Star className="h-8 w-8 text-yellow-300 ml-2" />
              </div>
              <p className="text-xl text-blue-100">
                Всё необходимое для успешной рекламы стоматологии
              </p>
            </div>

            <CardContent className="p-8">
              <div className="grid lg:grid-cols-2 gap-8">
                {/* Pricing */}
                <div className="space-y-6">
                  <div>
                    <h4 className="text-2xl font-bold text-gray-900 mb-4">Стоимость</h4>
                    
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                        <span className="text-gray-700 font-medium">Настройка (разовая)</span>
                        <span className="text-2xl font-bold text-blue-600">
                          {data.setup_fee.toLocaleString()}₽
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                        <span className="text-gray-700 font-medium">Ведение (ежемесячно)</span>
                        <span className="text-2xl font-bold text-green-600">
                          {data.monthly_fee.toLocaleString()}₽
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
                        <span className="text-gray-700 font-medium">Мин. рекламный бюджет</span>
                        <span className="text-2xl font-bold text-purple-600">
                          {data.min_budget.toLocaleString()}₽
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <div className="flex items-center mb-2">
                      <Star className="h-5 w-5 text-yellow-600 mr-2" />
                      <span className="font-semibold text-yellow-800">Специальное предложение</span>
                    </div>
                    <p className="text-yellow-700 text-sm">
                      При заключении договора до конца месяца — скидка 20% на настройку
                    </p>
                  </div>
                </div>

                {/* What's included */}
                <div>
                  <h4 className="text-2xl font-bold text-gray-900 mb-6">Что входит в стоимость</h4>
                  
                  <div className="space-y-3">
                    {data.includes.map((item, index) => (
                      <div key={index} className="flex items-start">
                        <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-3 mt-0.5">
                          <Check className="h-4 w-4 text-green-600" />
                        </div>
                        <span className="text-gray-700">{item}</span>
                      </div>
                    ))}
                  </div>

                  <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
                    <h5 className="font-bold text-gray-900 mb-2">Результат за первый месяц:</h5>
                    <ul className="text-sm text-gray-700 space-y-1">
                      <li>• Стоимость заявки от 350₽</li>
                      <li>• Конверсия 8-12%</li>
                      <li>• Первые заявки через 3-5 дней</li>
                      <li>• Полная настройка всех кампаний</li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* CTA */}
              <div className="mt-8 text-center">
                <Button 
                  onClick={onOpenForm}
                  size="lg"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-12 py-4 text-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 group"
                >
                  Начать сотрудничество
                  <ArrowRight className="ml-2 h-6 w-6 group-hover:translate-x-1 transition-transform" />
                </Button>
                
                <p className="mt-4 text-gray-600">
                  Бесплатная консультация • Расчет стоимости заявки • План продвижения
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Additional info */}
        <div className="mt-16 text-center">
          <div className="max-w-4xl mx-auto">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              Почему такая стоимость?
            </h3>
            
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-blue-600 font-bold">1</span>
                </div>
                <h4 className="font-bold text-gray-900 mb-2">Узкая специализация</h4>
                <p className="text-gray-600 text-sm">Работаю только со стоматологиями — знаю все нюансы ниши</p>
              </div>
              
              <div className="text-center">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-green-600 font-bold">2</span>
                </div>
                <h4 className="font-bold text-gray-900 mb-2">Проверенные методы</h4>
                <p className="text-gray-600 text-sm">Использую только работающие стратегии с доказанной эффективностью</p>
              </div>
              
              <div className="text-center">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-purple-600 font-bold">3</span>
                </div>
                <h4 className="font-bold text-gray-900 mb-2">Личная работа</h4>
                <p className="text-gray-600 text-sm">Все кампании настраиваю лично, без привлечения сторонних специалистов</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Pricing;