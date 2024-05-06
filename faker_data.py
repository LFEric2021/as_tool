import pandas as pd
from faker import Faker
import random
from datetime import timedelta, datetime


class FakeDataGenerator:
    def __init__(self, schema, enum_options=None, num_rows=100):
        self.schema = schema
        self.enum_options = enum_options or {'枚举值': ['A', 'B', 'C', 'D']}
        self.num_rows = num_rows
        self.fake = Faker()

    def generate_fake_data(self):
        data = []

        # 为每种数据类型创建一个生成函数
        type_to_generator = {
            'integer': lambda: self.fake.random_int(min=0, max=1000),
            'float': lambda: self.fake.random_number(digits=5, fix_len=False),
            'boolean': lambda: self.fake.boolean(),
            'enumerate': lambda field: random.choice(self.enum_options.get(field, ['A', 'B', 'C', 'D'])),
            'string': lambda: self.fake.name(),
            'datetime': lambda: self.fake.date_time_between(start_date="-30y", end_date="now"),
            'date': lambda: self.fake.date_time_between(start_date="-30y", end_date="now"),
        }

        # 生成数据
        for _ in range(self.num_rows):
            row = {column: type_to_generator[col_type](column) if col_type == 'enumerate' else type_to_generator[
                col_type]() for column, col_type in self.schema.items()}
            data.append(row)

        # 转换为DataFrame
        data = self.data_adjustment(pd.DataFrame(data))
        data['processing_time'] =  pd.Series(self.get_first_day_of_week(1, '2023-01-01')) 

        return data

    @staticmethod
    def data_adjustment(df):
        df['activate_to_active_cnt_1d'] = df['activate_org_cnt'].map(lambda x: int(x * random.uniform(0.01, 1)))
        df['activate_to_active_cnt_7d'] = df['activate_org_cnt'].map(lambda x: int(x * random.uniform(0.01, 1)))
        df['activate_to_active_cnt_30d'] = df['activate_org_cnt'].map(lambda x: int(x * random.uniform(0.01, 1)))

        df['active_to_retention_cnt_1d'] = df['active_org_cnt'].map(lambda x: int(x * random.uniform(0.01, 1)))
        df['active_to_retention_cnt_7d'] = df['active_org_cnt'].map(lambda x: int(x * random.uniform(0.01, 1)))
        df['active_to_retention_cnt_30d'] = df['active_org_cnt'].map(lambda x: int(x * random.uniform(0.01, 1)))

        df['subscriber_cnt'] = df['active_org_cnt'].map(lambda x: int(x * random.uniform(0.01, 1)))

        return df

    def get_first_day_of_week(self, day_of_week, start_date):
        """
        生成一个列表，包含多个日期，每个日期都是一周的第一天，且日期大于指定的开始日期。
        :param day_of_week: 输入的数字，1代表星期一，2代表星期二，依此类推。
        :param start_date: 指定的开始日期，格式为 'YYYY-MM-DD'。
        :param num_dates: 需要生成的日期数量。
        :return: 返回一个包含日期的列表。
        """
        fake = Faker()
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        dates = []

        while len(dates) < self.num_rows:
            # 生成一个随机日期，确保它在开始日期之后
            random_date = fake.date_between_dates(date_start=start_date, date_end= start_date + timedelta(days=500))
            # 计算周的第一天
            current_weekday = random_date.weekday()
            target_weekday = (day_of_week - 1) % 7
            days_difference = target_weekday - current_weekday
            first_day_of_week = random_date + timedelta(days=days_difference)

            # 如果生成的日期小于开始日期，则调整到下一个周期
            if first_day_of_week < start_date:
                first_day_of_week += timedelta(days=7)

            if first_day_of_week not in dates:  # 确保所有日期都是唯一的
                dates.append(first_day_of_week)

        return dates


    @staticmethod
    def save_to_excel(data, filename='./output/app_feature_usage_s_w.xlsx'):
        # 将DataFrame保存为Excel文件
        data.to_excel(filename, index=False)
        print(f"Data saved to {filename}")


if __name__ == "__main__":
    schema = {
        # 'processing_time': 'enumerate',
        'processing_time': 'date',
        'date_dim': 'enumerate',
        'features': 'enumerate',
        'marketing_segment': 'enumerate',
        'mrr_segment': 'enumerate',
        'industry': 'enumerate',
        'vertical': 'enumerate',
        'import_source ': 'enumerate',
        'contract_type': 'enumerate',
        'plan_group': 'enumerate',
        'cnt_type': 'enumerate',
        'activate_org_cnt': 'integer',
        'activate_to_active_cnt_1d': 'integer',
        'activate_to_active_cnt_7d': 'integer',
        'activate_to_active_cnt_30d': 'integer',
        'active_event_cnt': 'integer',
        'active_org_cnt': 'integer',
        'active_to_retention_cnt': 'integer',
        'subscriber_cnt': 'integer',
    }
    # 定义枚举值的选项
    enum_options = {
        'processing_time': [str(i) for i in range(202301, 202350)] + [str(i) for i in range(202301, 202320)],
        'features': ['Shipment_management_Carrier_auto_detection', 'Shipment_management_Import_shipment',
                     'Shipment_management_view', 'Shipment_management_Custom_shipment_tags',
                     'Shipment_management_Bulk_export_shipment_data', 'Shipment_management_Specific_event_filters',
                     'Shipment_management_Custom_field_filters', 'Shipment_management_Export_using_custom_format',
                     'Shipment_management_Carrier_auto-correction', 'Shipment_management_Recurring_dashboard_emails',
                     'Shipment_management_Tracking_dashboards', ],
        'marketing_segment': ['ENT - L', 'ENT - M', 'ENT - S', 'MM', 'SMB', 'SMB - S', 'Unknown'],
        'mrr_segment': ['ENT - L', 'ENT - M', 'ENT - S', 'MM', 'SMB', 'SMB - S', 'Unknown'],
        'industry': ['Industry_a', 'Industry_b', 'Industry_c', 'Industry_d', ],
        'vertical': ['Vertical_a', 'Vertical_b', 'Vertical_c', 'Vertical_d', ],
        'import_source ': ['source_a', 'source_b', 'source_c', 'source_d', ],
        'contract_type': ['Contract_a', 'Contract_b', 'Contract_c', 'Contract_d', ],
        'plan_group': ['essentials', 'pro', 'premium', 'enterprise', ],
        'cnt_type': ['organization', 'customer'],
        'date_dim': ['week', 'month']
    }

    # 创建一个FakeDataGenerator实例
    generator = FakeDataGenerator(schema, enum_options, num_rows=10000)

    # 生成数据
    fake_data = generator.generate_fake_data()

    # 保存到Excel文件
    generator.save_to_excel(fake_data)
