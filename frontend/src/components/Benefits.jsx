import React from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Award, FileText, Shield, Users } from 'lucide-react';

const iconMap = {
  Award,
  FileText,
  Shield,
  Users
};

const Benefits = ({ data }) => {
  return (
    <section id="benefits" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="bg-blue-100 text-blue-800 px-4 py-2 text-sm mb-4">
            Почему выбирают меня
          </Badge>
          <h2 className="text-3xl lg:text-5xl font-bold text-gray-900 mb-6">
            Мои преимущества
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            6+ лет я специализируюсь исключительно на продвижении стоматологий. 
            Знаю все нюансы ниши и гарантирую результат.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {data.map((benefit) => {
            const Icon = iconMap[benefit.icon];
            return (
              <Card key={benefit.id} className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg hover:-translate-y-2">
                <CardContent className="p-8 text-center">
                  <div className="mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:from-blue-600 group-hover:to-indigo-600 transition-all duration-300">
                      <Icon className="h-8 w-8 text-blue-600 group-hover:text-white transition-colors duration-300" />
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-4">
                    {benefit.title}
                  </h3>
                  
                  <p className="text-gray-600 leading-relaxed">
                    {benefit.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Trust signals */}
        <div className="mt-20">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">50+</div>
              <div className="text-gray-600">стоматологий работают со мной</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">6+</div>
              <div className="text-gray-600">лет специализации в нише</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600 mb-2">95%</div>
              <div className="text-gray-600">клиентов продлевают сотрудничество</div>
            </div>
          </div>
        </div>

        {/* Guarantee section */}
        <div className="mt-20">
          <Card className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200">
            <CardContent className="p-8 text-center">
              <div className="max-w-3xl mx-auto">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Shield className="h-8 w-8 text-green-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  Гарантия результата
                </h3>
                <p className="text-lg text-gray-700 mb-6">
                  Если в первый месяц мы не получим заявки дешевле вашей текущей стоимости 
                  (или если рекламы у вас нет — дешевле 800₽ за заявку), 
                  я верну 100% стоимости услуг.
                </p>
                <div className="flex items-center justify-center space-x-2 text-green-600 font-semibold">
                  <Shield className="h-5 w-5" />
                  <span>Работаю по договору как ИП</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default Benefits;