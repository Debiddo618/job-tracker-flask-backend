from flask import Blueprint, jsonify, request, g
from db_helpers import get_db_connection
import psycopg2
import psycopg2.extras

jobs_blueprint = Blueprint('jobs_blueprint', __name__)


# Show all jobs by a userid


@jobs_blueprint.route('/jobs/users/<user_id>')
def jobs_index(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM jobs WHERE user_id = %s", (user_id))
        jobs = cursor.fetchall()
        connection.close()
        return jobs
    except:
        return "Application Error", 500
    
@jobs_blueprint.route('/hello')
def hello_index():
    return 'Hello, World'

# Create a job


@jobs_blueprint.route('/jobs', methods=['POST'])
def create_jobs():
    try:
        new_job = request.json
        connection = get_db_connection()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("INSERT INTO jobs (title, company_name, job_location, type, salary, description, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *",
                       (new_job['title'], new_job['company_name'], new_job['job_location'], new_job['type'], new_job['salary'], new_job['description'], new_job['user_id']))
        created_job = cursor.fetchone()
        connection.commit()  # Commit changes to the database
        connection.close()
        return created_job, 201
    except Exception as e:
        return str(e), 500

# Show a job by id


@jobs_blueprint.route('/jobs/<job_id>', methods=['GET'])
def show_job(job_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
        job = cursor.fetchone()
        if job is None:
            connection.close()
            return "Job Not Found", 404
        connection.close()
        return job, 200
    except Exception as e:
        return str(e), 500

# Delete job by id


@jobs_blueprint.route('/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
        connection.commit()
        cursor.close()
        return {"id": job_id, "message": "Job deleted Successfully"}, 200
    except Exception as e:
        return str(e), 500

# Update job by id


@jobs_blueprint.route('/jobs/<job_id>', methods=['PUT'])
def update_job(job_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("UPDATE jobs SET title = %s, company_name = %s, job_location = %s, type = %s, salary = %s, description = %s WHERE id = %s RETURNING *",
                       (request.json['title'], request.json['company_name'], request.json['job_location'], request.json['type'], request.json['salary'], request.json['description'], job_id))
        updated_job = cursor.fetchone()
        if updated_job is None:
            return "Job Not Found", 404
        connection.commit()
        connection.close()
        return updated_job, 202
    except Exception as e:
        return str(e), 500
